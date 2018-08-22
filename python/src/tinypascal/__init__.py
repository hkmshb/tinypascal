# -*- coding: utf-8 -*-
import enum
import pkg_resources


def get_version():
    '''Returns the version details for tinypascal.
    '''
    packages = pkg_resources.require('tinypascal')
    return packages[0].version



class Token:

    class Type(enum.Enum):
        EOF = "EOF"
        PLUS = "PLUS"
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

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(Token.Type.EOF, None)

        current_char = text[self.pos]
        if current_char.isdigit():
            token = Token(Token.Type.INTEGER, int(current_char))
            self.pos += 1
            return token
        if current_char == '+':
            token = Token(Token.Type.PLUS, current_char)
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
        self.eat(Token.Type.INTEGER)

        op = self.current_token
        self.eat(Token.Type.PLUS)

        right = self.current_token
        self.eat(Token.Type.INTEGER)

        return left.value + right.value


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
