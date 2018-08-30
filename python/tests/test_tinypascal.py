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

    def test_failing_lexical_analysis(self):
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

    @pytest.mark.parametrize('expression, result', [
        ('2+5', 7), ('5 -2', 3), ('2- 5', -3),
        ('99 / 9', 11), ('2 + 2 - 1 * 6 / 2', 1)
    ])
    def test_expression_evaluation(self, expression, result):
        lxr = Lexer(expression)
        assert Interpreter(Parser(lxr)).run() == result
