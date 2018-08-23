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
    DIVIDE = "DIVIDE"
    MULTIPLY = "MULTIPLY"
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


class Interpreter:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = text[self.pos]

    def error(self, error_code=0):
        raise Exception('Error parsing input\n')

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
                    TokenType.MULTIPLY if self.current_char == '*' else
                    TokenType.DIVIDE
                )
                token = Token(token_type, self.current_char)
                self.advance()
                return token

            self.error()
        return Token(TokenType.EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        left, op, right = (None, None, None)
        self.current_token = self.get_next_token()

        while (
            self.current_token is not None and
            self.current_token.type != TokenType.EOF
        ):
            if left is None:
                left = self.current_token
                self.eat(TokenType.INTEGER)

            op = self.current_token
            if op.value in '+-*/':
                self.eat(op.type)

            right = self.current_token
            self.eat(TokenType.INTEGER)

            if op.type == TokenType.PLUS:
                result = left.value + right.value
            elif op.type == TokenType.MINUS:
                result = left.value - right.value
            elif op.type == TokenType.MULTIPLY:
                result = left.value * right.value
            elif op.type == TokenType.DIVIDE:
                result = left.value / right.value
            left = Token(TokenType.INTEGER, round(result))
        return left.value


def main():
    while True:
        try:
            text = input('calc> ')
        except IOError:
            break
        if not text:
            continue

        try:
            interpreter = Interpreter(text)
            result = interpreter.expr()
            print(result)
        except Exception as ex:
            print('error: {}'.format(ex))
            sys.exit()
