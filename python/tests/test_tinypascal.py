#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tinypascal import get_version, TokenType, Lexer, Parser, Interpreter



def test_version_detail():
    version = get_version()
    assert version == '0.1.dev0'


class TestLexer:

    def _assert_expected_token_types(self, lxr, token_types):
        for token_type in token_types:
            assert lxr.get_next_token().type == token_type

    def test_fails_for_empty_text(self):
        with pytest.raises(IndexError):
            lxr = Lexer('')
            assert lxr.get_next_token().type == TokenType.EOF

    def test_valid_lexical_analysis(self):
        lxr = Lexer('3 + 4')
        self._assert_expected_token_types(lxr, [
            TokenType.INTEGER, TokenType.PLUS,
            TokenType.INTEGER, TokenType.EOF
        ])

        lxr = Lexer('88 * 2 + 987')
        self._assert_expected_token_types(lxr, [
            TokenType.INTEGER, TokenType.MUL,
            TokenType.INTEGER, TokenType.PLUS,
            TokenType.INTEGER, TokenType.EOF
        ])

    def test_pascal_statement_lexical_analysis(self):
        lxr = Lexer("BEGIN a := 5; END.")
        self._assert_expected_token_types(lxr, [
            TokenType.BEGIN, TokenType.ID,
            TokenType.ASSIGN, TokenType.INTEGER,
            TokenType.SEMI, TokenType.END,
            TokenType.DOT
        ])


class TestInterpreter:

    @pytest.mark.parametrize('expression, result', [
        ('BEGIN x := 2+5; END.', 7),
        ('BEGIN x := 5 -2; END.', 3),
        ('BEGIN x := 2- 5; END.', -3),
        ('BEGIN x := 99 / 9; END.', 11),
        ('BEGIN x := 2 + 2 - 1 * 6 / 2; END.', 1)
    ])
    def test_expression_evaluation(self, expression, result):
        lxr = Lexer(expression)
        it = Interpreter(Parser(lxr))
        it.run()
        assert 'x' in it.GLOBAL_SCOPE and it.GLOBAL_SCOPE['x'] == result

    def test_fails_for_invalid_expression(self):
        with pytest.raises(Exception):  # missing operator
            lxr = Lexer('92 1')
            self._assert_expected_token_types(lxr, [
                TokenType.INTEGER, TokenType.INTEGER
            ])

            # reset in preparation for calling expr
            lxr.pos = 0
            Interpreter(Parser(lxr)).run()

        with pytest.raises(Exception):  # invalid token order
            lxr = Lexer('+ 92 1')
            self._assert_expected_token_types(lxr, [
                TokenType.PLUS, TokenType.INTEGER, TokenType.INTEGER,
                TokenType.EOF
            ])

            # reset pos & call expr
            lxr.pos = 0
            Interpreter(Parser(lxr)).run()

    def test_basic_pascal_code(self):
        code = """
        BEGIN
            BEGIN
                number := 2;
                a := number;
                b := 10 * a + 10 * number / 4;
                c := a - - b
            END;
            x := 11;
        END.
        """
        lxr = Lexer(code)
        it = Interpreter(Parser(lxr))
        it.run()
        assert 'number' in it.GLOBAL_SCOPE and it.GLOBAL_SCOPE['number'] == 2
        assert 'a' in it.GLOBAL_SCOPE and it.GLOBAL_SCOPE['a'] == 2
        assert 'b' in it.GLOBAL_SCOPE and it.GLOBAL_SCOPE['b'] == 25
        assert 'c' in it.GLOBAL_SCOPE and it.GLOBAL_SCOPE['c'] == 27
        assert 'x' in it.GLOBAL_SCOPE and it.GLOBAL_SCOPE['x'] == 11
