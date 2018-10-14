import unittest
from core.recognizer import calculation
from math import *


class GoodTests(unittest.TestCase):

    def test_operation_priority(self):
        self.assertEqual(5, calculation("1+2*2"))

    def test_operation_priority1(self):
        self.assertEqual(25, calculation("1+(2+3*2)*3"))

    def test_operation_priority2(self):
        self.assertEqual(30, calculation("10*(2+1)"))

    def test_operation_priority3(self):
        self.assertEqual(1000, calculation("10**(2+1)"))

    def test_operation_priority4(self):
        self.assertEqual(100 / 3 ** 2, calculation("100/3**2"))

    def test_operation_priority5(self):
        self.assertEqual(100 / 3 % 2 ** 2, calculation("100/3%2**2"))

    def test_functions_and_constants(self):
        self.assertEqual(pi + e, calculation("pi+e"))

    def test_functions_and_constants1(self):
        self.assertEqual(1, calculation("log(e)"))

    def test_functions_and_constants2(self):
        self.assertEqual(1, calculation("sin(pi/2)"))

    def test_functions_and_constants3(self):
        self.assertEqual(2, calculation("log10(100)"))

    def test_functions_and_constants4(self):
        self.assertEqual(sin(pi/2)*1116, calculation("sin(pi/2)1116"))

    def test_functions_and_constants5(self):
        self.assertEqual(2, calculation("2*sin(pi/2)"))

    def test_associative(self):
        self.assertEqual(102 % 12 % 7, calculation("102%12%7"))

    def test_associative1(self):
        self.assertEqual(100/4/3, calculation("100/4/3"))

    def test_associative2(self):
        self.assertEqual(2 ** 3 ** 4, calculation("2**3**4"))

    def test_comparison_operators(self):
        self.assertEqual(1 + 2 * 3 == 1 + 2 * 3, calculation("1+2*3==1+2*3"))

    def test_comparison_operators1(self):
        self.assertEqual(e ** 5 >= e ** 5 + 1, calculation("e**5>=e**5+1"))

    def test_comparison_operators2(self):
        self.assertEqual(1 + 24 // 3 + 1 != 1 + 24 // 3 + 2, calculation("1+24/3+1!=1+24/3+2"))

    def test_common_tests(self):
        self.assertEqual(100, calculation("(100)"))
    def test_common_tests1(self):
        self.assertEqual(666, calculation("666"))
    def test_common_tests2(self):
        self.assertEqual(30, calculation("10(2+1)"))
    def test_common_tests3(self):
        self.assertEqual(-0.1, calculation("-.1"))
    def test_common_tests4(self):
        self.assertEqual(1. / 3, calculation("1/3"))
    def test_common_tests5(self):
        self.assertEqual(1.0/3.0, calculation("1.0/3.0"))
    def test_common_tests6(self):
        self.assertEqual(.1 * 2.0**56.0, calculation(".1 * 2.0**56.0"))
    def test_common_tests7(self):
        self.assertEqual(e**34, calculation("e**34"))
    def test_common_tests8(self):
        self.assertEqual((2.0**(pi/pi+e/e+2.0**0.0)), calculation("(2.0**(pi/pi+e/e+2.0**0.0))"))
    def test_common_tests9(self):
        self.assertEqual((2.0**(pi/pi+e/e+2.0**0.0))**(1.0/3.0),
                         calculation("(2.0**(pi/pi+e/e+2.0**0.0))**(1.0/3.0)"))

    def test_common_tests10(self):
        self.assertEqual(sin(pi/2**1) + log(1*4+2**2+1, 3**2),
                         calculation("sin(pi/2**1) + log(1*4+2**2+1, 3**2)"))

    def test_common_tests11(self):
        self.assertEqual(10*e**0.*log10(.4* -5/ -0.1-10) - -abs(-53//10) + -5,
                         calculation("10*e^0*log10(.4* -5/ -0.1-10) - -abs(-53//10) + -5"))

    def test_common_tests12(self):
        self.assertEqual(sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0),
                         calculation("sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0**2.0))))--cos(1.0)--cos(0.0)**3.0)"))

    def test_common_tests13(self):
        self.assertEqual(2.0**(2.0**2.0*2.0**2.0), calculation("2.0**(2.0**2.0*2.0**2.0)"))

    def test_common_tests14(self):
        self.assertEqual(sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e))),
                         calculation("sin(e**log(e**e**sin(23.0),45.0) + cos(3.0+log10(e**-e)))"))


class RaisesTest(unittest.TestCase):
    def test_raise(self):
        self.assertRaises(Exception, calculation, "")
    def test_raise1(self):
        self.assertRaises(Exception, calculation, "+")
    def test_raise2(self):
        self.assertRaises(Exception, calculation, "1-")
    def test_raise3(self):
        self.assertRaises(Exception, calculation, "1 2")
    def test_raise4(self):
        self.assertRaises(Exception, calculation, "ee")
    def test_raise5(self):
        self.assertRaises(Exception, calculation, "123e")
    def test_raise6(self):
        self.assertRaises(Exception, calculation, "==7")
    def test_raise7(self):
        self.assertRaises(Exception, calculation, "1 * * 2")
    def test_raise8(self):
        self.assertRaises(Exception, calculation, "1 + 2(3 * 4))")
    def test_raise9(self):
        self.assertRaises(Exception, calculation, "((1+2)")
    def test_raise10(self):
        self.assertRaises(Exception, calculation, "1 + 1 2 3 4 5 6 ")
    def test_raise11(self):
        self.assertRaises(Exception, calculation, "log100(100)")
    def test_raise12(self):
        self.assertRaises(Exception, calculation, "------")
    def test_raise13(self):
        self.assertRaises(Exception, calculation, "5 > = 6")
    def test_raise14(self):
        self.assertRaises(Exception, calculation, "5 / / 6")
    def test_raise15(self):
        self.assertRaises(Exception, calculation, "6 < = 6")
    def test_raise16(self):
        self.assertRaises(Exception, calculation, "6 * * 6")
    def test_raise17(self):
        self.assertRaises(Exception, calculation, "(((((")


if __name__ == '__main__':
    unittest.main()