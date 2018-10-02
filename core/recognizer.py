from core.operatios import available_functions, available_operations, available_order_symbols


class Delimiters:
    pass


class Digit:
    pass


class Operator:
    pass


class MathExpr:
    pass


class Scope:
    pass


class OpenScope(Scope):
    pass


class CloseScope(Scope):
    pass


class Expression:
    class Node:
        left = None
        right = None
        operation = None
        values = None

    @classmethod
    def add_value(cls, obj):
        pass

    @classmethod
    def add_operator(cls, obj):
        pass

    @classmethod
    def solve(cls):
        while cls.first_order_operators:
            operation = cls.first_order_operators.pop()

        cls.expr = []





class MathExpression:
    def __init__(self, math_expr, rules):
        self.math_expr = math_expr.replace(" ", "")
        self.rules = rules

    def get_type(self, symbol):
        if symbol.isdigit():
            sym_type = Digit
        elif symbol == "(":
            sym_type = OpenScope
        elif symbol == ")":
            sym_type = CloseScope
        elif symbol.isalpha():
            sym_type = MathExpr
        else:
            sym_type = Operator
        return sym_type

    def to_lexems(self):
        sym_type = self.get_type(self.math_expr[0])
        lexem = self.math_expr[0]
        lexems = []
        for symbol in self.math_expr[1:]:
            next_type = self.get_type(symbol)
            if issubclass(next_type, Scope):
                pass
            elif symbol == "." and issubclass(sym_type, Digit) or issubclass(next_type, Digit) and lexem[-1] == ".":
                lexem += symbol
                continue
            elif sym_type == next_type:
                lexem += symbol
                continue
            lexems.append(lexem)
            sym_type = next_type
            lexem = symbol
        lexems.append(lexem)
        return lexems

    def check_lexems(self, lexems, deep=False):
        expression = Expression()
        len_lexems = len(lexems)
        i = 0
        while i <= len_lexems:
            lexem = lexems[i]
            if lexems in available_operations:
                operation = available_operations[lexem]
                expression.append(operation)

            elif lexem in available_functions:
                if lexems[i + 1] not in available_order_symbols:
                    raise ValueError
                arguments = self.get_argument_for_function(lexems[i + 1])
                func = available_functions[lexem]
                try:
                    result = func.calculate(arguments)
                    expression.append(result)
                except AttributeError:
                    raise Exception("Too many arguments")

            elif lexem in available_order_symbols:
                if lexem == "(":
                    child_expr = self.check_lexems(lexems[i + 1], deep=True)
                    expression.extend(child_expr)
                elif lexem == ")" and deep:
                    return expression.solve()
                else:
                    raise SyntaxError("Can't find opened function before closed")

            else:
                try:
                    try:
                        num = float(lexem)
                    except ValueError:
                        num = int(lexem)
                    expression.append(num)
                except ValueError:
                    raise TypeError(f"lexem {lexem} is not recognized")
        if deep:
            raise SyntaxError("Can't find closed scope")

        return expression.solve()

    def get_argument_for_function(self, lexems):
        close_scope_is_finded = False
        arguments = []
        sub_expression = []
        for lexem in lexems:
            if Delimiters.check(lexem):
                argument = self.check_lexems(sub_expression)
                arguments.append(argument)
                sub_expression = []
                continue
            elif lexem == ")":
                return arguments
            else:
                sub_expression.append(lexem)

        if not close_scope_is_finded:
            raise SyntaxError("Can't Find Closed Scope")




class Recognizer:
    SCOPE_OPEN = "("
    SCOPE_CLOSE = ")"

    class CalculateResult:
        def __init__(self, operation, result_string):
            self.operation = operation
            self.result_string = result_string

    def __init__(self, math_expr=None):
        self.str_math_expr = math_expr

    def _spread_space_between_tokens(self, expr):
        result_str = ""
        for s in expr:
            if s == "+" or s == "*" or s == self.SCOPE_CLOSE or s == self.SCOPE_OPEN:
                result_str += f" {s} "
            elif s.isdigit():
                result_str += s
        return result_str.strip()

    def get_lexems(self, expr):
        lexems = self._spread_space_between_tokens(expr)
        return lexems.split(" ")

    def apply_operator(self, expr, operator):
        stack = []
        lexems = self.get_lexems(expr)

        for lexem in lexems:
            stack.append(lexem)

            if len(stack) >= 3:
                left = stack[len(stack) - 3]
                middle = stack[len(stack) - 2]
                right = stack[len(stack) - 1]

                if left.isdigit() and middle == operator and right.isdigit():
                    left_digit = int(left)
                    right_digit = int(right)
                    res = 0
                    if middle == "*":
                        res = left_digit * right_digit
                    elif middle == "+":
                        res = left_digit + right_digit

                    stack.pop(-1)
                    stack.pop(-1)
                    stack.pop(-1)
                    stack.append(str(res))
        stack = list(map(lambda x: str(x), stack))
        return "".join(stack)

    def eval_expr_without_parens(self, expr_without_parens):
        result = self.apply_operator(expr_without_parens, "*")
        result = self.apply_operator(result, "+")
        return result

    def open_single_paren(self, expr):
        result = self.CalculateResult(False, expr)
        lexems = self.get_lexems(expr)
        lexems = list(filter(lambda x: x != "", lexems))
        stack = []
        lpindex = 0
        for index, lexem in enumerate(lexems):
            stack.append(lexem)
            if lexem == self.SCOPE_OPEN:
                lpindex = index
            if lexem == self.SCOPE_CLOSE and not result.operation:
                stack.pop(len(stack) - 1)
                number_of_item_to_pop = index - lpindex - 1
                ewp = ""
                for _ in range(number_of_item_to_pop):
                    ewp += stack.pop(len(stack) - 1)
                ewp_eval_result = self.eval_expr_without_parens(ewp)
                stack.pop(len(stack) - 1)
                stack.append(ewp_eval_result)
                result.operation = True
        result.result_string = "".join(stack)

        return result

    def calculate(self, expr):
        result = self.CalculateResult(False, expr)
        while True:
            result = self.open_single_paren(result.result_string)
            if not result.operation:
                break

        result.result_string = self.eval_expr_without_parens(result.result_string)

        return result.result_string


if __name__ == "__main__":
    # r = Recognizer()
    # print(r.calculate("2+++7"))

    # m = MathExpression("sum(1,2,3)sum(1,2,3)123++-+-+-+++-+++18.90900", None)
    Expression.append(2)
    Expression.append(lambda x, y: x*y)
    Expression.append(2)
    Expression.append(lambda x, y: x+y)
    Expression.append(2)
    Expression.solve()

    # print(m.to_lexems())
