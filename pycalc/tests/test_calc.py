import unittest
from math import *
from unittest.mock import patch

from pycalc.core.available_names import available_functions, available_constants
from pycalc.core.exceptions import TooManyBrackets, TooManySpaces, UnrecognizedLexem, TooManyArguments, \
    UnrecognizedOperator, NotEnoughArguments, EmptyExpression
from pycalc.core.recognizer import calculation


class GoodTests(unittest.TestCase):

    def test_unary_operators(self):
        self.assertEqual(-13, calculation("-13", available_functions, available_constants))

    def test_unary_operators1(self):
        self.assertEqual(19, calculation("6-(-13)", available_functions, available_constants))

    def test_unary_operators2(self):
        self.assertEqual(0, calculation("1---1", available_functions, available_constants))

    def test_unary_operators3(self):
        self.assertEqual(-1, calculation("-+---+-1", available_functions, available_constants))

    def test_operation_priority(self):
        self.assertEqual(5, calculation("1+2*2", available_functions, available_constants))

    def test_operation_priority1(self):
        self.assertEqual(25, calculation("1+(2+3*2)*3", available_functions, available_constants))

    def test_operation_priority2(self):
        self.assertEqual(30, calculation("10*(2+1)", available_functions, available_constants))

    def test_operation_priority3(self):
        self.assertEqual(1000, calculation("10**(2+1)", available_functions, available_constants))

    def test_operation_priority4(self):
        self.assertEqual(100 / 3 ** 2, calculation("100/3**2", available_functions, available_constants))

    def test_operation_priority5(self):
        self.assertEqual(100 / 3 % 2 ** 2, calculation("100/3%2**2", available_functions, available_constants))

    def test_functions_and_constants(self):
        self.assertEqual(pi + e, calculation("pi+e", available_functions, available_constants))

    def test_functions_and_constants1(self):
        self.assertEqual(1, calculation("log(e)", available_functions, available_constants))

    def test_functions_and_constants2(self):
        self.assertEqual(1, calculation("sin(pi/2)", available_functions, available_constants))

    def test_functions_and_constants3(self):
        self.assertEqual(2, calculation("log10(100)", available_functions, available_constants))

    def test_functions_and_constants4(self):
        self.assertEqual(sin(pi / 2) * 1116, calculation("sin(pi/2)1116", available_functions, available_constants))

    def test_functions_and_constants5(self):
        self.assertEqual(2, calculation("2*sin(pi/2)", available_functions, available_constants))

    def test_associative(self):
        self.assertEqual(102 % 12 % 7, calculation("102%12%7", available_functions, available_constants))

    def test_associative1(self):
        self.assertEqual(100 / 4 / 3, calculation("100/4/3", available_functions, available_constants))

    def test_associative2(self):
        self.assertEqual(2 ** 3 ** 4, calculation("2**3**4", available_functions, available_constants))

    def test_comparison_operators(self):
        self.assertEqual(1 + 2 * 3 == 1 + 2 * 3, calculation("1+2*3==1+2*3", available_functions, available_constants))

    def test_comparison_operators1(self):
        self.assertEqual(e ** 5 >= e ** 5 + 1, calculation("e**5>=e**5+1", available_functions, available_constants))

    def test_comparison_operators2(self):
        self.assertEqual(1 + 24 // 3 + 1 != 1 + 24 // 3 + 2,
                         calculation("1+24/3+1!=1+24/3+2", available_functions, available_constants))

    def test_common_tests(self):
        self.assertEqual(100, calculation("(100)", available_functions, available_constants))

    def test_common_tests1(self):
        self.assertEqual(666, calculation("666", available_functions, available_constants))

    def test_common_tests2(self):
        self.assertEqual(30, calculation("10(2+1)", available_functions, available_constants))

    def test_common_tests3(self):
        self.assertEqual(-0.1, calculation("-.1", available_functions, available_constants))

    def test_common_tests4(self):
        self.assertEqual(1. / 3, calculation("1/3", available_functions, available_constants))

    def test_common_tests5(self):
        self.assertEqual(1.0 / 3.0, calculation("1.0/3.0", available_functions, available_constants))

    def test_common_tests6(self):
        self.assertEqual(.1 * 2.0 ** 56.0, calculation(".1 * 2.0**56.0", available_functions, available_constants))

    def test_common_tests7(self):
        self.assertEqual(e ** 34, calculation("e**34", available_functions, available_constants))

    def test_common_tests8(self):
        self.assertEqual((2.0 ** (pi / pi + e / e + 2.0 ** 0.0)),
                         calculation("(2.0**(pi/pi+e/e+2.0**0.0))", available_functions, available_constants))

    def test_common_tests9(self):
        self.assertEqual((2.0 ** (pi / pi + e / e + 2.0 ** 0.0)) ** (1.0 / 3.0),
                         calculation("(2.0**(pi/pi+e/e+2.0**0.0))**(1.0/3.0)", available_functions,
                                     available_constants))

    def test_common_tests10(self):
        self.assertEqual(sin(pi / 2 ** 1) + log(1 * 4 + 2 ** 2 + 1, 3 ** 2),
                         calculation("sin(pi/2**1) + log(1*4+2**2+1, 3**2)", available_functions, available_constants))

    def test_common_tests11(self):
        self.assertEqual(10 * e ** 0. * log10(.4 * -5 / -0.1 - 10) - -abs(-53 // 10) + -5,
                         calculation("10*e^0*log10(.4* -5/ -0.1-10) - -abs(-53//10) + -5", available_functions,
                                     available_constants))

    def test_common_tests12(self):
        self.assertEqual(
            sin(-cos(
                -sin(3.0) - cos(-sin(-3.0 * 5.0) - sin(cos(log10(43.0)))) + cos(sin(sin(34.0 - 2.0 ** 2.0)))) - -cos(
                1.0) - -cos(0.0) ** 3.0),
            calculation(
                "sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))"
                "+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0)",
                available_functions, available_constants))

    def test_common_tests13(self):
        self.assertEqual(2.0 ** (2.0 ** 2.0 * 2.0 ** 2.0),
                         calculation("2.0**(2.0**2.0*2.0**2.0)", available_functions, available_constants))

    def test_common_tests14(self):
        self.assertEqual(sin(e ** log(e ** e ** sin(23.0), 45.0) + cos(3.0 + log10(e ** -e))),
                         calculation("sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e)))", available_functions,
                                     available_constants))

    def test_common_tests15(self):
        self.assertEqual(10, calculation("max(1,2,10,max(1,2,3))", available_functions, available_constants))

    def test_builtin_func_test15(self):
        self.assertEqual(1.5, calculation("round(1.5, 1)", available_functions, available_constants))

    def test_builtin_func_test16(self):
        self.assertEqual(4, calculation("pow(2, 2)", available_functions, available_constants))

    def test_builtin_func_test17(self):
        self.assertEqual(1.5, calculation("abs(-1.5)", available_functions, available_constants))


class ImportModulesTest(unittest.TestCase):

    def setUp(self):
        self.available_functions = available_functions.copy()
        self.available_constants = available_constants.copy()

    def update_functions_and_constants(self, funcs=None, const=None):
        self.available_functions.update(funcs or {})
        self.available_constants.update(const or {})

    @patch("pycalc.core.utils.add_available_names_from_module")
    def test_import_module1(self, add_available_names_from_module):
        side_effect = {
            "side_effect": self.update_functions_and_constants(
                funcs={"bar": lambda x, y: x + y ** y ** y + x},
                const={"x": 1, "y": 2})
        }
        add_available_names_from_module.configure_mock(**side_effect)
        add_available_names_from_module(available_functions, available_constants, "test_module")
        self.assertEqual(18, calculation("bar(x,y)", self.available_functions, self.available_constants))

    @patch("pycalc.core.utils.add_available_names_from_module")
    def test_import_module2(self, add_available_names_from_module):
        side_effect = {
            "side_effect": self.update_functions_and_constants(const={"x": 4, "y": 2})
        }
        add_available_names_from_module.configure_mock(**side_effect)
        add_available_names_from_module(available_functions, available_constants, "test_module")
        self.assertEqual(32, calculation("10+x+y**x+y", self.available_functions, self.available_constants))

    @patch("pycalc.core.utils.add_available_names_from_module")
    def test_import_module3(self, add_available_names_from_module):
        side_effect = {
            "side_effect": self.update_functions_and_constants(
                funcs={"bar": lambda x: x ** x ** x + x * x // x})
        }
        add_available_names_from_module.configure_mock(**side_effect)
        add_available_names_from_module(available_functions, available_constants, "test_module")
        self.assertEqual(8, calculation("bar(2) - 10", self.available_functions, self.available_constants))


class RaisesTest(unittest.TestCase):
    def test_raise(self):
        self.assertRaises(EmptyExpression, calculation, "", available_functions, available_constants)

    def test_raise1(self):
        self.assertRaises(NotEnoughArguments, calculation, "+", available_functions, available_constants)

    def test_raise2(self):
        self.assertRaises(NotEnoughArguments, calculation, "1-", available_functions, available_constants)

    def test_raise3(self):
        self.assertRaises(TooManySpaces, calculation, "1 2", available_functions, available_constants)

    def test_raise4(self):
        self.assertRaises(UnrecognizedLexem, calculation, "ee", available_functions, available_constants)

    def test_raise5(self):
        self.assertRaises(UnrecognizedOperator, calculation, "123e", available_functions, available_constants)

    def test_raise6(self):
        self.assertRaises(NotEnoughArguments, calculation, "==7", available_functions, available_constants)

    def test_raise7(self):
        self.assertRaises(TooManySpaces, calculation, "1 * * 2", available_functions, available_constants)

    def test_raise8(self):
        self.assertRaises(TooManyBrackets, calculation, "1 + 2(3 * 4))", available_functions, available_constants)

    def test_raise9(self):
        self.assertRaises(TooManyBrackets, calculation, "((1+2)", available_functions, available_constants)

    def test_raise10(self):
        self.assertRaises(TooManySpaces, calculation, "1 + 1 2 3 4 5 6 ", available_functions, available_constants)

    def test_raise11(self):
        self.assertRaises(UnrecognizedLexem, calculation, "log100(100)", available_functions, available_constants)

    def test_raise12(self):
        self.assertRaises(NotEnoughArguments, calculation, "------", available_functions, available_constants)

    def test_raise13(self):
        self.assertRaises(TooManySpaces, calculation, "5 > = 6", available_functions, available_constants)

    def test_raise14(self):
        self.assertRaises(TooManySpaces, calculation, "5 / / 6", available_functions, available_constants)

    def test_raise15(self):
        self.assertRaises(TooManySpaces, calculation, "6 < = 6", available_functions, available_constants)

    def test_raise16(self):
        self.assertRaises(TooManySpaces, calculation, "6 * * 6", available_functions, available_constants)

    def test_raise17(self):
        self.assertRaises(TooManyBrackets, calculation, "(((((", available_functions, available_constants)

    def test_raise18(self):
        self.assertRaises(TooManyArguments, calculation, "sin(1,2)", available_functions, available_constants)

    def test_raise19(self):
        self.assertRaises(UnrecognizedLexem, calculation, "foo(2)", available_functions, available_constants)

    def test_raise20(self):
        self.assertRaises(UnrecognizedOperator, calculation, "max(1,2,10max(1,2,3))", available_functions,
                          available_constants)

    def test_raise21(self):
        self.assertRaises(TooManyArguments, calculation, "sin(,)", available_functions, available_constants)
