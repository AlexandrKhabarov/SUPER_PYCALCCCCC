import unittest

import math

from pycalc.core.calculator import calculate


class GoodTests(unittest.TestCase):
    def test_uanry_operators(self):
        test_cases = [
            ("-13", -13),
            ("6-(-13)", 19),
            ("1---1", 0),
            ("-+---+-1", -1),
        ]

        for source, expected_result in test_cases:
            self._assert_calculation(source, expected_result)

    def test_operation_priority(self):
        test_cases = [
            ("1+2*2", 1 + 2 * 2),
            ("1+(2+3*2)*3", 1 + (2 + 3 * 2) * 3),
            ("10*(2+1)", 10 * (2 + 1)),
            ("10**(2+1)", 10 ** (2 + 1)),
            ("100/3**2", 100 / 3 ** 2),
            ("100/3%2**2", 100 / 3 % 2 ** 2),
        ]

        for source, expected_result in test_cases:
            self._assert_calculation(source, expected_result)

    def test_functions_and_constants(self):
        test_cases = [
            ("pi+e", math.pi + math.e),
            ("log(e)", math.log(math.e)),
            ("sin(pi/2)", math.sin(math.pi / 2)),
            ("log10(100)", math.log10(100)),
            ("sin(pi/2)1116", math.sin(math.pi / 2) * 1116),
            ("2*sin(pi/2)", 2 * math.sin(math.pi / 2)),
        ]

        for source, expected_result in test_cases:
            self._assert_calculation(source, expected_result)

    def test_associative_operations(self):
        test_cases = [
            ("102%12%7", 102 % 12 % 7),
            ("100/4/3", 100 / 4 / 3),
            ("2**3**4", 2 ** 3 ** 4),
        ]

        for source, expected_result in test_cases:
            self._assert_calculation(source, expected_result)

    def test_comparison(self):
        test_cases = [
            ("1+23==1+23", 1 + 23 == 1 + 23),
            ("e**5>=e**5+1", math.e ** 5 >= math.e ** 5 + 1),
            ("1+24/3+1!=1+24/3+2", 1 + 24 / 3 + 1 != 1 + 24 / 3 + 2),
        ]

        for source, expected_result in test_cases:
            self._assert_calculation(source, expected_result)

    def test_common(self):
        test_cases = [
            ("(100)", 100),
            ("666", 666),
            ("10(2+1)", 10 * (2 + 1)),
            ("-.1", -.1),
            ("1/3", 1 / 3),
            ("1.0/3.0", 1.0 / 3.0),
            (".1 * 2.0**56.0", .1 * 2.0 ** 56.0),
            ("e**34", math.e ** 34),
            ("(2.0**(pi/pi+e/e+2.0**0.0))", (2.0 ** (math.pi / math.pi + math.e / math.e + 2.0 ** 0.0))),
            ("(2.0**(pi/pi+e/e+2.0**0.0))**(1.0/3.0)",
             (2.0 ** (math.pi / math.pi + math.e / math.e + 2.0 ** 0.0)) ** (1.0 / 3.0)),
            ("sin(pi/2**1) + log(1*4+2**2+1, 3**2)", math.sin(math.pi / 2 ** 1) + math.log(1 * 4 + 2 ** 2 + 1, 3 ** 2)),
            ("10e^0log10(.4* -5/ -0.1-10) - -abs(-53/10) + -5",
             10 * math.e ** 0 * math.log10(.4 * -5 / -0.1 - 10) - -abs(-53 / 10) + -5),
            (
                "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0)",
                (math.sin(-math.cos(-math.sin(3.0) - math.cos(-math.sin(-3.0 * 5.0)
                                                              - math.sin(math.cos(math.log10(43.0))))
                                    + math.cos(math.sin(math.sin(34.0 - 2.0 ** 2.0))))
                          - -math.cos(1.0) - -math.cos(0.0) ** 3.0))),
            ("2.0**(2.0**2.0*2.0**2.0)", 2.0 ** (2.0 ** 2.0 * 2.0 ** 2.0)),
            ("sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e)))",
             math.sin(math.e ** math.log(math.e ** math.e ** math.sin(23.0), 45.0)
                      + math.cos(3.0 + math.log10(math.e ** -math.e)))),
        ]

        for source, expected_result in test_cases:
            self._assert_calculation(source, expected_result)

    def test_error_cases(self):
        test_cases = [
            "",
            "+",
            "1-",
            "1 2",
            "ee",
            "123e",
            "==7",
            "1 * * 2",
            "1 + 2(3 * 4))",
            "((1+2)",
            "1 + 1 2 3 4 5 6 ",
            "log100(100)",
            "------",
            "5 > = 6",
            "5 / / 6",
            "6 < = 6",
            "6 * * 6",
            "(((((",
        ]

        for source in test_cases:
            with self.assertRaises(Exception):
                self._assert_calculation(source, None)

    def _assert_calculation(self, source, expected_result):
        with self.subTest(msg=source):
            result = calculate(source)
            self.assertEqual(result, expected_result)
