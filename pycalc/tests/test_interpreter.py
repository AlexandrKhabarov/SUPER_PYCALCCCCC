import unittest

from pycalc.core.expressions import Unary, Literal, Binary, Grouping, Interpreter
from pycalc.core.token_types import TokenTypes
from pycalc.core.tokens import Token


class InterpreterTestCase(unittest.TestCase):
    def test_interpreter(self):
        test_cases = [
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

        expected_results = [
            -13,
            19,
            0,
            -1,
            5,
            25
        ]

        for a, e, in zip(test_cases, expected_results):
            self._test_parser(a, e)

    def _test_parser(self, tree, expected_result):
        with self.subTest(f"Tested expression:"):
            interpreter = Interpreter()
            result = interpreter.evaluate(tree)
            self.assertEqual(result, expected_result)
