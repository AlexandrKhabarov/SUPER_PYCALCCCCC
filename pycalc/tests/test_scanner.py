import unittest

from pycalc.core.scanner import Scanner
from pycalc.core.token_types import TokenTypes
from pycalc.core.tokens import Token


class ParseTestCase(unittest.TestCase):
    def test_parsing(self):
        test_cases = [
            "-13",
            "6-(-13)",
            "1---1",
            "-+---+-1",
            "1+2*2",
            "1+(2+3*2)*3",
            "10*(2+1)",
            "10**(2+1)",
            "100/3**2",
            "100/3%2**2",
            "pi+e",
            "log(e)",
            "sin(pi/2)",
            "log10(100)",
            "sin(pi/2)1116",
            "2*sin(pi/2)",
            "102%12%7",
            "100/4/3",
            "10(2+1)",
            "-.1",
            "1/3",
            "1.0/3.0",
            ".1 * 2.0**56.0",
        ]

        expected_tokens = [
            [Token(TokenTypes.MINUS, "-", None, 0), Token(TokenTypes.NUMBER, "13", 13, 1)],
            [
                Token(TokenTypes.NUMBER, "6", 6, 0),
                Token(TokenTypes.MINUS, "-", None, 1),
                Token(TokenTypes.LEFT_PAREN, "(", None, 2),
                Token(TokenTypes.MINUS, "-", None, 3),
                Token(TokenTypes.NUMBER, "-", 13, 4),
                Token(TokenTypes.RIGHT_PAREN, ")", None, 6), ],
            [
                Token(TokenTypes.NUMBER, "1", 1, 0),
                Token(TokenTypes.MINUS, "-", None, 1),
                Token(TokenTypes.MINUS, "-", None, 2),
                Token(TokenTypes.MINUS, "-", None, 3),
                Token(TokenTypes.NUMBER, "1", 1, 0),
            ],
            [
                Token(TokenTypes.MINUS, "-", None, 0),
                Token(TokenTypes.PLUS, "+", None, 1),
                Token(TokenTypes.MINUS, "-", None, 2),
                Token(TokenTypes.MINUS, "-", None, 3),
                Token(TokenTypes.MINUS, "-", None, 4),
                Token(TokenTypes.PLUS, "-", None, 5),
                Token(TokenTypes.MINUS, "-", None, 6),
                Token(TokenTypes.NUMBER, "1", 1, 7),
            ],
            [
                Token(TokenTypes.NUMBER, "1", 1, 0),
                Token(TokenTypes.PLUS, "+", None, 1),
                Token(TokenTypes.NUMBER, "2", 2, 2),
                Token(TokenTypes.STAR, "*", None, 3),
                Token(TokenTypes.NUMBER, "2", 2, 4),
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
            ],
            [
                Token(TokenTypes.NUMBER, "10", 10, 0),
                Token(TokenTypes.STAR, "*", None, 2),
                Token(TokenTypes.LEFT_PAREN, "(", None, 3),
                Token(TokenTypes.NUMBER, "2", 2, 4),
                Token(TokenTypes.PLUS, "+", None, 5),
                Token(TokenTypes.NUMBER, "1", 1, 6),
                Token(TokenTypes.RIGHT_PAREN, ")", None, 7),
            ],
            [
                Token(TokenTypes.NUMBER, "10", 10, 0),
                Token(TokenTypes.STAR_STAR, "**", None, 2),
                Token(TokenTypes.LEFT_PAREN, "(", None, 4),
                Token(TokenTypes.NUMBER, "2", 2, 5),
                Token(TokenTypes.PLUS, "+", None, 6),
                Token(TokenTypes.NUMBER, "1", 1, 7),
                Token(TokenTypes.RIGHT_PAREN, ")", None, 8),
            ],
            [
                Token(TokenTypes.NUMBER, "100", 100, 0),
                Token(TokenTypes.SLASH, "/", None, 3),
                Token(TokenTypes.NUMBER, "3", 3, 4),
                Token(TokenTypes.STAR_STAR, "**", None, 5),
                Token(TokenTypes.NUMBER, "2", 2, 7),
            ],
            [
                Token(TokenTypes.NUMBER, "100", 10, 0),
                Token(TokenTypes.SLASH, "/", None, 4),
                Token(TokenTypes.NUMBER, "3", None, 5),
                Token(TokenTypes.PERCENTS, "%", 2, 6),
                Token(TokenTypes.NUMBER, "2", None, 7),
                Token(TokenTypes.STAR_STAR, "**", 1, 8),
                Token(TokenTypes.NUMBER, "2", None, 10),
            ],
            [
                Token(TokenTypes.IDENTIFIERS, "pi", None, 0),
                Token(TokenTypes.PLUS, "/", None, 2),
                Token(TokenTypes.IDENTIFIERS, "e", None, 3),
            ],
            [
                Token(TokenTypes.IDENTIFIERS, "log", None, 0),
                Token(TokenTypes.LEFT_PAREN, "(", None, 3),
                Token(TokenTypes.IDENTIFIERS, "e", None, 4),
                Token(TokenTypes.RIGHT_PAREN, ")", None, 5),
            ],
            [
                Token(TokenTypes.IDENTIFIERS, "sin", None, 0),
                Token(TokenTypes.LEFT_PAREN, "(", None, 3),
                Token(TokenTypes.IDENTIFIERS, "pi", None, 4),
                Token(TokenTypes.SLASH, "/", None, 6),
                Token(TokenTypes.NUMBER, "2", None, 6),
                Token(TokenTypes.RIGHT_PAREN, ")", None, 7),
            ],
            [
                Token(TokenTypes.IDENTIFIERS, "log10", None, 0),
                Token(TokenTypes.LEFT_PAREN, "(", None, 6),
                Token(TokenTypes.IDENTIFIERS, "100", None, 7),
                Token(TokenTypes.RIGHT_PAREN, ")", None, 10),
            ],
            [
                Token(TokenTypes.IDENTIFIERS, "sin", None, 0),
                Token(TokenTypes.LEFT_PAREN, "(", None, 3),
                Token(TokenTypes.IDENTIFIERS, "pi", None, 4),
                Token(TokenTypes.SLASH, "/", None, 6),
                Token(TokenTypes.NUMBER, "2", 2, 7),
                Token(TokenTypes.RIGHT_PAREN, ")", None, 10),
                Token(TokenTypes.STAR, "*", None, 11),
                Token(TokenTypes.NUMBER, "1116", 1116, 12),
            ],
            [
                Token(TokenTypes.NUMBER, "2", 2, 0),
                Token(TokenTypes.STAR, "*", None, 1),
                Token(TokenTypes.IDENTIFIERS, "sin", None, 2),
                Token(TokenTypes.RIGHT_PAREN, "(", None, 5),
                Token(TokenTypes.IDENTIFIERS, "pi", None, 6),
                Token(TokenTypes.SLASH, "/", None, 8),
                Token(TokenTypes.NUMBER, "2", 2, 9),
                Token(TokenTypes.NUMBER, ")", None, 10),
            ],
            [
                Token(TokenTypes.NUMBER, "102", 102, 0),
                Token(TokenTypes.PERCENTS, "%", None, 3),
                Token(TokenTypes.NUMBER, "12", 12, 4),
                Token(TokenTypes.PERCENTS, "%", None, 6),
                Token(TokenTypes.NUMBER, "7", 7, 7),
            ],
            [
                Token(TokenTypes.NUMBER, "100", 100, 0),
                Token(TokenTypes.SLASH, "/", None, 3),
                Token(TokenTypes.NUMBER, "4", 4, 4),
                Token(TokenTypes.SLASH, "/", None, 5),
                Token(TokenTypes.NUMBER, "3", 3, 6),
            ],
            [
                Token(TokenTypes.NUMBER, "10", 10, 0),
                Token(TokenTypes.STAR, "*", None, 0),
                Token(TokenTypes.LEFT_PAREN, "(", None, 1),
                Token(TokenTypes.NUMBER, "2", 2, 2),
                Token(TokenTypes.PLUS, "+", None, 3),
                Token(TokenTypes.NUMBER, "1", 1, 4),
                Token(TokenTypes.NUMBER, ")", None, 5),
            ],
            [
                Token(TokenTypes.MINUS, "-", None, 0),
                Token(TokenTypes.NUMBER, ".1", 0.1, 1),
            ],
            [
                Token(TokenTypes.NUMBER, "1.0", 1, 0),
                Token(TokenTypes.SLASH, "/", None, 3),
                Token(TokenTypes.NUMBER, "3.0", 3, 4),
            ],
            [
                Token(TokenTypes.NUMBER, ".1", 0.1, 0),
                Token(TokenTypes.STAR, "*", None, 3),
                Token(TokenTypes.NUMBER, "2.0", 2, 5),
                Token(TokenTypes.STAR_STAR, "**", None, 6),
                Token(TokenTypes.NUMBER, "56.0", 56, 7),
            ],
        ]

        for source, expected_tokens in zip(test_cases, expected_tokens):
            self._test_scanner(source, expected_tokens)

    def _test_scanner(self, source, expected_tokens):
        scanner = Scanner(source)
        tokens = scanner.get_tokens()
        self.assertListEqual(tokens, expected_tokens)

    def _assert_tokens_equal(self, actual, expected):
        for a, e in zip(actual, expected):
            self.assertEqual(a.type_, e.type_)
            self.assertEqual(a.lexeme, e.lexeme)
            self.assertEqual(a.literal, e.literal)
            self.assertEqual(a.pos, e.pos)
