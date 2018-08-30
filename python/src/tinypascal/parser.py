from .lexer import TokenType


class AST:
    '''Base class for all nodes within an Abstract-Syntax Tree.
    '''
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Compound(AST):
    '''Represents a 'BEGIN ... END' block.
    '''
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    '''The Var node is constructed out of ID token.
    '''
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self, error_code=0):
        raise Exception('Error parsing input')

    def eat(self, token_type):
        # compares the current token with the passed in token type and if
        # they match then `eat` the current token and assign the ntext
        # token ...
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        '''factor : PLUS factor
                  | MINUS factor
                  | INTEGER
                  | LPAREN expr RPAREN
                  | variable
        '''
        token = self.current_token
        if token.type == TokenType.PLUS:
            self.eat(TokenType.PLUS)
            return UnaryOp(token, self.factor())
        if token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return UnaryOp(token, self.factor())
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            return self.variable()

    def term(self):
        '''term: factor ((MUL | DIV) factor)*
        '''
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOp(node, token, self.factor())
        return node

    def expr(self):
        '''Arithmetic expression parser / interpreter.

        calc> 9 + 8 - 3 * 5
        2

        expr:   term ((PLUS | MINUS) term)*
        term:   factor ((MUL | DIV) factor)*
        factor: INTEGER
        '''
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(node, token, self.term())
        return node

    def empty(self):
        '''An empty production.
        '''
        return NoOp()

    def variable(self):
        '''variable : ID
        '''
        token = self.current_token
        self.eat(TokenType.ID)
        return Var(token)

    def assignment_statement(self):
        '''assignment_statement : variable ASSIGN expr
        '''
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        return Assign(left, token, right)

    def statement(self):
        '''statement : compound_statement
                     | assignment_statement
                     | empty
        '''
        if self.current_token.type == TokenType.BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == TokenType.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def statement_list(self):
        '''statement_list : statement
                          | statement SEMI statement_list
        '''
        results = [self.statement()]
        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())

        if self.current_token.type == TokenType.ID:
            self.error()

        return results

    def compound_statement(self):
        '''compound_statement: BEGIN statement_list END
        '''
        self.eat(TokenType.BEGIN)
        nodes = self.statement_list()
        self.eat(TokenType.END)

        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root

    def program(self):
        '''program: compound_statement DOT
        '''
        node = self.compound_statement()
        self.eat(TokenType.DOT)
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.EOF:
            self.error()
        return node
