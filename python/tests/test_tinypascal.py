#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from tinypascal import get_version, Interpreter, TokenType


def test_version_detail():
    version = get_version()
    assert version == '0.1.dev0'


class TestInterpreter:

    def _assert_expected_token_types(self, it, token_types):
        for token_type in token_types:
            assert it.get_next_token().type == token_type

    def test_fails_for_empty_text(self):
        with pytest.raises(IndexError):
            it = Interpreter('')
            assert it.get_next_token().type == TokenType.EOF

    def test_valid_lexical_analysis(self):
        it = Interpreter('3 + 4')
        self._assert_expected_token_types(it, [
            TokenType.INTEGER, TokenType.PLUS,
            TokenType.INTEGER, TokenType.EOF
        ])

        it = Interpreter('88 * 2 + 987')
        self._assert_expected_token_types(it, [
            TokenType.INTEGER, TokenType.MULTIPLY,
            TokenType.INTEGER, TokenType.PLUS,
            TokenType.INTEGER, TokenType.EOF
        ])

    def test_failing_lexical_analysis(self):
        with pytest.raises(Exception):  # missing operator
            it = Interpreter('92 1')
            self._assert_expected_token_types(it, [
                TokenType.INTEGER, TokenType.INTEGER
            ])

            # reset in preparation for calling expr
            it.pos = 0
            it.expr()

        with pytest.raises(Exception):  # invalid token order
            it = Interpreter('+ 92 1')
            self._assert_expected_token_types(it, [
                TokenType.PLUS, TokenType.INTEGER, TokenType.INTEGER,
                TokenType.EOF
            ])

            # reset pos & call expr
            it.pos = 0
            it.expr()

    @pytest.mark.parametrize('expression, result', [
        ('2+5', 7), ('5 -2', 3), ('2- 5', -3),
        ('99 / 9', 11), ('2 + 2 - 1 * 6 / 2', 9)
    ])
    def test_expression_evaluation(self, expression, result):
        it = Interpreter(expression)
        assert it.expr() == result
