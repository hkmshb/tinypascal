# -*- coding: utf-8 -*-
import sys
import pkg_resources


def get_version():
    '''Returns the version details for tinypascal.
    '''
    packages = pkg_resources.require('tinypascal')
    return packages[0].version



class Token:
    # token type constants
    EOF = "EOF"
    PLUS = "PLUS"
    MINUS = "MINUS"
    INTEGER = "INTEGER"

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

    def error(self, error_code=0):
        print('error: Error parsing input\n')
        sys.exit(error_code)

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(Token.EOF, None)

        self._suppress_whitespace()
        current_char = text[self.pos]

        if current_char.isdigit():
            digits = self._read_digits()
            token = Token(Token.INTEGER, int(digits))
            self.pos += 1
            return token
        if current_char in '+-':
            token_type = Token.PLUS if current_char == '+' else Token.MINUS
            token = Token(token_type, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()
        left = self.current_token
        self.eat(Token.INTEGER)

        op = self.current_token
        if op.value in '+-':
            self.eat(op.type)

        right = self.current_token
        self.eat(Token.INTEGER)

        if op.type == Token.PLUS:
            return left.value + right.value
        if op.type == Token.MINUS:
            return left.value - right.value
        self.error()

    def _read_digits(self):
        digits = []
        current_char = self.text[self.pos]
        while current_char.isdigit():
            digits.append(current_char)
            self.pos += 1
            if self.pos >= len(self.text):
                break
            current_char = self.text[self.pos]

        self.pos -= 1   # need to adjust pos to last digit
        return ''.join(digits)

    def _suppress_whitespace(self):
        current_char = self.text[self.pos]
        while current_char.isspace():
            self.pos += 1
            current_char = self.text[self.pos]


def main():
    while True:
        try:
            text = input('calc> ')
        except IOError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)
