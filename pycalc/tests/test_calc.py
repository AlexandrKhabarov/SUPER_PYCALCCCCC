import unittest

import math

from pycalc.core.calculator import calculate


class TestCase:
    def __init__(self, *, tested_expression, expected_result):
        self.tested_expression = tested_expression
        self.expected_result = expected_result


class IntegrationTests(unittest.TestCase):
    def test_unary_operators(self):
        test_cases = [
            TestCase(
                tested_expression="-13",
                expected_result=-13
            ),
            TestCase(
                tested_expression="6-(-13)",
                expected_result=19
            ),
            TestCase(
                tested_expression="1---1",
                expected_result=0
            ),
            TestCase(
                tested_expression="-+---+-1",
                expected_result=-1
            ),
        ]

        self._check_test_cases(test_cases)

    def test_operation_priority(self):
        test_cases = [
            TestCase(
                tested_expression="1+2*2",
                expected_result=5
            ),
            TestCase(
                tested_expression="1+(2+3*2)*3",
                expected_result=25
            ),
            TestCase(
                tested_expression="10*(2+1)",
                expected_result=30
            ),
            TestCase(
                tested_expression="10**(2+1)",
                expected_result=1000
            ),
            TestCase(
                tested_expression="100/2**2",
                expected_result=25
            ),
            TestCase(
                tested_expression="100/2%2**2",
                expected_result=2
            ),
        ]

        self._check_test_cases(test_cases)

    def test_functions_and_constants(self):
        test_cases = [
            TestCase(
                tested_expression="pi+e",
                expected_result=math.pi + math.e
            ),
            TestCase(
                tested_expression="log(e)",
                expected_result=math.log(math.e)
            ),
            TestCase(
                tested_expression="sin(pi/2)",
                expected_result=math.sin(math.pi / 2)
            ),
            TestCase(
                tested_expression="log10(100)",
                expected_result=math.log10(100)
            ),
            TestCase(
                tested_expression="sin(pi/2)*1116",
                expected_result=math.sin(math.pi / 2) * 1116
            ),
            TestCase(
                tested_expression="2*sin(pi/2)",
                expected_result=2 * math.sin(math.pi / 2)
            ),
        ]

        self._check_test_cases(test_cases)

    def test_associative_operations(self):
        test_cases = [
            TestCase(
                tested_expression="102%12%7",
                expected_result=102 % 12 % 7
            ),
            TestCase(
                tested_expression="100/4/3",
                expected_result=100 / 4 / 3
            ),
            TestCase(
                tested_expression="2**3**4",
                expected_result=2 ** 3 ** 4
            ),
        ]

        self._check_test_cases(test_cases)

    def test_comparison(self):
        test_cases = [
            TestCase(
                tested_expression="1+23==1+23",
                expected_result=True
            ),
            TestCase(
                tested_expression="e**5>=e**5+1",
                expected_result=False
            ),
            TestCase(
                tested_expression="1+24/3+1!=1+24/3+2",
                expected_result=True
            ),
        ]

        self._check_test_cases(test_cases)

    def test_common(self):
        test_cases = [
            TestCase(
                tested_expression="(100)",
                expected_result=100
            ),
            TestCase(
                tested_expression="666",
                expected_result=666
            ),
            TestCase(
                tested_expression="10*(2+1)",
                expected_result=10 * (2 + 1)
            ),
            TestCase(
                tested_expression="-.1",
                expected_result=-.1
            ),
            TestCase(
                tested_expression="1/3",
                expected_result=1 / 3
            ),
            TestCase(
                tested_expression="1.0/3.0",
                expected_result=1.0 / 3.0
            ),
            TestCase(
                tested_expression=".1 * 2.0**56.0",
                expected_result=.1 * 2.0 ** 56.0
            ),
            TestCase(
                tested_expression="e**34",
                expected_result=math.e ** 34
            ),
            TestCase(
                tested_expression="(2.0**(pi/pi+e/e+2.0**0.0))",
                expected_result=(2.0 ** (math.pi / math.pi + math.e / math.e + 2.0 ** 0.0))
            ),
            TestCase(
                tested_expression="(2.0**(pi/pi+e/e+2.0**0.0))**(1.0/3.0)",
                expected_result=(2.0 ** (math.pi / math.pi + math.e / math.e + 2.0 ** 0.0)) ** (1.0 / 3.0)
            ),
            TestCase(
                tested_expression="sin(pi/2**1) + log(1*4+2**2+1, 3**2)",
                expected_result=math.sin(math.pi / 2 ** 1) + math.log(1 * 4 + 2 ** 2 + 1, 3 ** 2)),
            TestCase(
                tested_expression="10*e^0*log10(.4* -5/ -0.1-10) - -abs(-53/10) + -5",
                expected_result=10 * math.e ** 0 * math.log10(.4 * -5 / -0.1 - 10) - -abs(-53 / 10) + -5
            ),
            TestCase(
                tested_expression="sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))"
                                  "+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0)",
                expected_result=(math.sin(-math.cos(-math.sin(3.0)
                                                    - math.cos(-math.sin(-3.0 * 5.0)
                                                               - math.sin(math.cos(math.log10(43.0))))
                                                    + math.cos(math.sin(math.sin(34.0 - 2.0 ** 2.0))))
                                          - -math.cos(1.0) - -math.cos(0.0) ** 3.0))
            ),
            TestCase(
                tested_expression="2.0**(2.0**2.0*2.0**2.0)",
                expected_result=2.0 ** (2.0 ** 2.0 * 2.0 ** 2.0)
            ),
            TestCase(
                tested_expression="sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e)))",
                expected_result=math.sin(math.e ** math.log(math.e ** math.e ** math.sin(23.0), 45.0)
                                         + math.cos(3.0 + math.log10(math.e ** -math.e)))
            ),
        ]

        self._check_test_cases(test_cases)

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
            with self.assertRaises(Exception, msg=source):
                calculate(source)

    def _check_test_cases(self, test_cases):
        for test_case in test_cases:
            self._assert_calculation(test_case)

    def _assert_calculation(self, test_case):
        tested_expression = test_case.tested_expression
        expected_result = test_case.expected_result
        with self.subTest(msg=tested_expression):
            result = calculate(tested_expression)
            self.assertEqual(result, expected_result)
