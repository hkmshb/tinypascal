import enum


class TokenType(enum.Enum):
    EOF = "EOF"
    LPAREN = "("
    RPAREN = ")"
    INTEGER = "INTEGER"
    MINUS = "MINUS"
    PLUS = "PLUS"
    DIV = "DIV"
    MUL = "MUL"
    BEGIN = "BEGIN"
    END = "END"
    DOT = "DOT"
    ID = "ID"
    ASSIGN = "ASSIGN"
    SEMI = "SEMI"


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        '''String representation of class instance.

        Examples:
            Token(TokenType.INTEGER, 3)
            Token(TokenType.PLUS, '+')
            Token(TokenType.DIV, '/')
        '''
        return "Token ({type}, {value})".format(
            type=self.type, value=self.value
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    "BEGIN": Token(TokenType.BEGIN, "BEGIN"),
    "END": Token(TokenType.END, "END")
}


class Lexer:

    def __init__(self, text):
        # client string input, e.g: "3 * 5", "9 + 2 - 3 * 5"
        self.text = text
        # self.pos is index into client string input, self.text
        self.pos = 0
        self.current_char = text[self.pos]

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        '''Advance the `pos` pointer and set the `current_char` variable.
        '''
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_integer(self):
        '''Return a multidigit integer consumed from the input.
        '''
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        '''Handle identifiers and reserved keywords.
        '''
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return RESERVED_KEYWORDS.get(result, Token(TokenType.ID, result))

    def get_next_token(self):
        '''Lexical analyser (aka scanner or tokenizer)

        This method is repsonsible for breaking an expression apart into
        tokens. One token at a time.
        '''
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.get_integer())

            if self.current_char in '+-*/()':
                token_type = (
                    TokenType.PLUS if self.current_char == '+' else
                    TokenType.MINUS if self.current_char == '-' else
                    TokenType.MUL if self.current_char == '*' else
                    TokenType.DIV if self.current_char == '/' else
                    TokenType.LPAREN if self.current_char == '(' else
                    TokenType.RPAREN
                )
                token = Token(token_type, self.current_char)
                self.advance()
                return token

            if self.current_char.isalpha():
                return self._id()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMI, ';')

            if self.current_char == '.':
                self.advance()
                return Token(TokenType.DOT, '.')

            self.error()
        return Token(TokenType.EOF, None)
