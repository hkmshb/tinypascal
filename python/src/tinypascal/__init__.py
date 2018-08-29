# -*- coding: utf-8 -*-
import sys
import pkg_resources
from .lexer import Lexer
from .parser import Parser



def get_version():
    '''Returns the version details for tinypascal.
    '''
    packages = pkg_resources.require('tinypascal')
    return packages[0].version


class Interpreter:

    def __init__(self, parser):
        self.parser = parser

    def run(self):
        return self.parser.parse()


def main():
    while True:
        try:
            text = input('calc> ')
        except IOError:
            break
        if not text:
            continue

        try:
            parser = Parser(Lexer(text))
            interpreter = Interpreter(parser)
            tree = interpreter.run()
            print_tree(tree)
        except Exception as ex:
            print('error: {}'.format(ex))
            raise ex
            sys.exit()


def print_tree(root):
    from .parser import BinOp, Num

    def walk(node):
        if isinstance(node, BinOp):
            print(node.op.value)
            walk(node.left)
            walk(node.right)
            print()
        else:
            print("%s " % node.value, end='')

    walk(root)
