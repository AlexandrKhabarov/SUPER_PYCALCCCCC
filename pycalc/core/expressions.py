import abc

from pycalc.core.environment import Environment, Callable
from pycalc.core.errors import runtime_error
from pycalc.core.token_types import TokenTypes


class Expr(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor):
        pass


class Call(Expr):
    def __init__(self, callable_, paren, arguments):
        self.callable_ = callable_
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor):
        return visitor.visit_call_expr(self)


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)


class Interpreter:
    def __init__(self):
        self.globals = Environment()

    def visit_variable_expr(self, expr):
        return self.globals.get(expr.name)

    def visit_call_expr(self, expr):
        callable_ = self.evaluate(expr.callable_)
        arguments = []

        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))

        if not isinstance(callable_, Callable):
            runtime_error(callable_, "Can only call functions")

        return callable_.call(arguments)

    def visit_literal_expr(self, expr: Literal):
        return expr.value

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: Unary):
        right = self.evaluate(expr.right)

        if expr.operator.type_ == TokenTypes.MINUS:
            right = self.evaluate(expr.right)
            self.check_number_operand(expr.operator, right)
            return -float(right)
        elif expr.operator.type_ == TokenTypes.PLUS:
            right = self.evaluate(expr.right)
            self.check_number_operand(expr.operator, right)
            return +right
        elif expr.operator.type_ == TokenTypes.NOT:
            return not self.is_truthy(right)

    def visit_binary_expr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type_ == TokenTypes.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.type_ == TokenTypes.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.type_ == TokenTypes.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.type_ == TokenTypes.PLUS:
            self.check_number_operands(expr.operator, left, right)
            return left + right
        elif expr.operator.type_ == TokenTypes.CAP or expr.operator.type_ == TokenTypes.STAR_STAR:
            self.check_number_operands(expr.operator, left, right)
            return left ** right
        elif expr.operator.type_ == TokenTypes.SLASH_SLASH:
            self.check_number_operands(expr.operator, left, right)
            return left // right
        elif expr.operator.type_ == TokenTypes.PERCENTS:
            self.check_number_operands(expr.operator, left, right)
            return left % right
        elif expr.operator.type_ == TokenTypes.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        elif expr.operator.type_ == TokenTypes.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        elif expr.operator.type_ == TokenTypes.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        elif expr.operator.type_ == TokenTypes.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        elif expr.operator.type_ == TokenTypes.NOT_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return not self.is_equal(left, right)
        elif expr.operator.type_ == TokenTypes.EQUAL_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return self.is_equal(left, right)

    def check_number_operand(self, operator, operand):
        if not isinstance(operand, (float, int)):
            runtime_error(operator, "Operand must be number.")

    def check_number_operands(self, operator, left, right):
        self.check_number_operand(operator, left)
        self.check_number_operand(operator, right)

    def is_truthy(self, obj):
        if obj is None or isinstance(obj, bool):
            return bool(obj)
        return True

    def is_equal(self, a, b):
        return a == b

    def evaluate(self, expr):
        return expr.accept(self)
