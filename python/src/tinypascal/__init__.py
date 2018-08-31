# -*- coding: utf-8 -*-
import sys
import pkg_resources
from .lexer import Lexer, TokenType
from .parser import Parser


def get_version():
    '''Returns the version details for tinypascal.
    '''
    packages = pkg_resources.require('tinypascal')
    return packages[0].version


class NodeVisitor:

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):

    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_UnaryOp(self, node):
        if node.op.type == TokenType.PLUS:
            return + self.visit(node.expr)
        if node.op.type == TokenType.MINUS:
            return - self.visit(node.expr)

    def visit_Num(self, node):
        return node.value

    def visit_NoOp(self, node):
        pass

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        return val

    def run(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    while True:
        try:
            text = input('tinypascal> ')
        except IOError:
            break
        if not text:
            continue

        try:
            parser = Parser(Lexer(text))
            interpreter = Interpreter(parser)
            interpreter.run()
            print(interpreter.GLOBAL_SCOPE)
        except Exception as ex:
            print('error: {}'.format(ex))
            sys.exit()
