# -*- coding: utf-8 -*-
import sys
import enum
import pkg_resources


def get_version():
    '''Returns the version details for tinypascal.
    '''
    packages = pkg_resources.require('tinypascal')
    return packages[0].version


class TokenType(enum.Enum):
    EOF = "EOF"
    PLUS = "PLUS"
    MINUS = "MINUS"
    DIV = "DIV"
    MUL = "MUL"
    INTEGER = "INTEGER"


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token ({type}, {value})".format(
            type=self.type, value=self.value
        )

    def __repr__(self):
        return self.__str__()


class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos]

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.get_integer())

            if self.current_char in '+-*/':
                token_type = (
                    TokenType.PLUS if self.current_char == '+' else
                    TokenType.MINUS if self.current_char == '-' else
                    TokenType.MUL if self.current_char == '*' else
                    TokenType.DIV
                )
                token = Token(token_type, self.current_char)
                self.advance()
                return token

            self.error()
        return Token(TokenType.EOF, None)


class Interpreter:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self, error_code=0):
        raise Exception('Error parsing input')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def term(self):
        token = self.current_token
        self.eat(TokenType.INTEGER)
        return token.value

    def expr(self):
        result = self.term()

        while self.current_token.type in (
            TokenType.PLUS, TokenType.MINUS,
            TokenType.MUL, TokenType.DIV
        ):
            if self.lexer.current_char.isspace():
                self.lexer.skip_whitespace()
                continue

            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.term()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result -= self.term()
            elif token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                result *= self.term()
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
                result /= self.term()
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except IOError:
            break
        if not text:
            continue

        try:
            interpreter = Interpreter(Lexer(text))
            result = interpreter.expr()
            print(result)
        except Exception as ex:
            print('error: {}'.format(ex))
            sys.exit()
