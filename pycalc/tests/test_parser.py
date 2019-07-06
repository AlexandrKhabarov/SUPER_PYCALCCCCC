import unittest

from pycalc.core.expressions import Unary, Binary, Grouping, Literal
from pycalc.core.parser import Parser
from pycalc.core.token_types import TokenTypes
from pycalc.core.tokens import Token


class ParserTestCase(unittest.TestCase):
    def test_parser(self):
        test_cases = [
            [
                Token(TokenTypes.MINUS, "-", None, 0),
                Token(TokenTypes.NUMBER, "13", 13, 1),
                Token(TokenTypes.EOF, "", None, 1),
            ],
            [
                Token(TokenTypes.NUMBER, "6", 6, 0),
                Token(TokenTypes.MINUS, "-", None, 1),
                Token(TokenTypes.LEFT_PAREN, "(", None, 2),
                Token(TokenTypes.MINUS, "-", None, 3),
                Token(TokenTypes.NUMBER, "13", 13, 4),
                Token(TokenTypes.RIGHT_PAREN, ")", None, 6),
                Token(TokenTypes.EOF, "", None, 6),
            ],
            [
                Token(TokenTypes.NUMBER, "1", 1, 0),
                Token(TokenTypes.MINUS, "-", None, 1),
                Token(TokenTypes.MINUS, "-", None, 2),
                Token(TokenTypes.MINUS, "-", None, 3),
                Token(TokenTypes.NUMBER, "1", 1, 4),
                Token(TokenTypes.EOF, "", None, 4),
            ],
            [
                Token(TokenTypes.MINUS, "-", None, 0),
                Token(TokenTypes.PLUS, "+", None, 1),
                Token(TokenTypes.MINUS, "-", None, 2),
                Token(TokenTypes.MINUS, "-", None, 3),
                Token(TokenTypes.MINUS, "-", None, 4),
                Token(TokenTypes.PLUS, "+", None, 5),
                Token(TokenTypes.MINUS, "-", None, 6),
                Token(TokenTypes.NUMBER, "1", 1, 7),
                Token(TokenTypes.EOF, "", None, 7),
            ],
            [
                Token(TokenTypes.NUMBER, "1", 1, 0),
                Token(TokenTypes.PLUS, "+", None, 1),
                Token(TokenTypes.NUMBER, "2", 2, 2),
                Token(TokenTypes.STAR, "*", None, 3),
                Token(TokenTypes.NUMBER, "2", 2, 4),
                Token(TokenTypes.EOF, "", None, 4),
            ],
            [
                Token(TokenTypes.NUMBER, "1", 1, 0),
                Token(TokenTypes.PLUS, "+", None, 1),
                Token(TokenTypes.LEFT_PAREN, "(", None, 2),
                Token(TokenTypes.NUMBER, "2", 2, 3),
                Token(TokenTypes.PLUS, "+", None, 4),
                Token(TokenTypes.NUMBER, "3", 3, 5),
                Token(TokenTypes.STAR, "*", None, 6),
                Token(TokenTypes.NUMBER, "2", 2, 7),
                Token(TokenTypes.RIGHT_PAREN, ")", None, 8),
                Token(TokenTypes.STAR, "*", None, 9),
                Token(TokenTypes.NUMBER, "3", 3, 10),
                Token(TokenTypes.EOF, "", None, 10),
            ],
        ]

        expected_trees = [
            Unary(
                Token(TokenTypes.MINUS, "-", None, 0),
                Literal(13)
            ),
            Binary(
                Literal(6),
                Token(TokenTypes.MINUS, "-", None, 1),
                Grouping(
                    Unary(
                        Token(TokenTypes.MINUS, "-", None, 3),
                        Literal(13),
                    )
                )
            ),
            Binary(
                Literal(1),
                Token(TokenTypes.MINUS, "-", None, 1),
                Unary(
                    Token(TokenTypes.MINUS, "-", None, 2),
                    Unary(
                        Token(TokenTypes.MINUS, "-", None, 3),
                        Literal(1),
                    )
                )
            ),
            Unary(
                Token(TokenTypes.MINUS, "-", None, 0),
                Unary(
                    Token(TokenTypes.PLUS, "+", None, 1),
                    Unary(
                        Token(TokenTypes.MINUS, "-", None, 2),
                        Unary(
                            Token(TokenTypes.MINUS, "-", None, 3),
                            Unary(
                                Token(TokenTypes.MINUS, "-", None, 4),
                                Unary(
                                    Token(TokenTypes.PLUS, "+", None, 5),
                                    Unary(
                                        Token(TokenTypes.MINUS, "-", None, 6),
                                        Literal(1),
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            Binary(
                Literal(1),
                Token(TokenTypes.PLUS, "+", None, 1),
                Binary(
                    Literal(2),
                    Token(TokenTypes.STAR, "*", None, 3),
                    Literal(2),
                )
            ),
            Binary(
                Literal(1),
                Token(TokenTypes.PLUS, "+", None, 1),
                Binary(
                    Grouping(
                        Binary(
                            Literal(2),
                            Token(TokenTypes.PLUS, "+", None, 4),
                            Binary(
                                Literal(3),
                                Token(TokenTypes.STAR, "*", None, 6),
                                Literal(2),
                            )
                        )
                    ),
                    Token(TokenTypes.STAR, "*", None, 9),
                    Literal(3),
                )
            )
        ]

        for a, e, in zip(test_cases, expected_trees):
            self._test_parser(a, e)

    def _test_parser(self, tokens, expected_tree):
        with self.subTest(f"Tested expression: '{' || '.join(map(str, tokens))}'"):
            parser = Parser(tokens)
            tree = parser.parse()
            self._assert_trees_equal(tree, expected_tree)

    def _assert_trees_equal(self, actual, expected_tree):
        getter = AstGetter()
        for a, e in zip(getter.get(actual), getter.get(expected_tree)):
            self.assertEqual(a, e)


class AstGetter:
    def get(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize(expr.expression)

    def visit_literal_expr(self, expr: Literal):
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.right)

    def parenthesize(self, *exprs):
        literals = []
        for expr in exprs:
            literals.append(expr.accept(self))

        return literals
