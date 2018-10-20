from core.available_names import available_functions, available_constants
from core.exceptions import TooManySpaces, TooManyBrackets, TooManyArguments, UnrecognizedOperator, UnrecognizedLexem, \
    UnrecognizedFunc
from core.operatios import available_operations, available_order_symbols
from core.types import Digit, Operator, MathExpr, Scope, OpenScope, CloseScope


class ExpressionCalculator:
    @classmethod
    def calc(cls, polish, args=False):
        stack = []
        for token in polish:
            if token in available_operations:
                operation = available_operations[token]
                if operation.co_arguments == 2:
                    y, x = stack.pop(), stack.pop()
                    stack.append(operation.func(x, y))
                elif operation.co_arguments == 1:
                    y = stack.pop()
                    stack.append(operation.func(y))
            else:
                stack.append(token)
        if not args and len(stack) > 1:
            raise UnrecognizedOperator()
        return stack[0] if len(stack) == 1 else stack

    @classmethod
    def shunting_yard(cls, parsed_formula):
        stack = []
        opened_scope = 0
        closed_scope = 0
        for token in parsed_formula:
            if token in available_operations:
                operation = available_operations[token]
                if operation.is_right_associated:
                    while stack and stack[-1] != "(" and operation.priority <= available_operations[stack[-1]].priority:
                        yield stack.pop()
                    stack.append(token)
                elif not operation.is_right_associated:
                    while stack and stack[-1] != "(" and operation.priority < available_operations[stack[-1]].priority:
                        yield stack.pop()
                    stack.append(token)
            elif token == ")":
                closed_scope += 1
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                opened_scope += 1
                stack.append(token)
            else:
                yield token

        if opened_scope - closed_scope != 0:
            raise TooManyBrackets()
        while stack:
            yield stack.pop()


class MathExpressionParser:
    def __init__(self, math_expr, rules=None):
        self.check_spaces(math_expr)
        self.math_expr = math_expr.replace(" ", "")
        self.rules = rules

    def check_spaces(self, math_expr):
        for i, ch in enumerate(math_expr):
            t = self.get_type(ch)
            if issubclass(t, Digit) or issubclass(t, MathExpr):
                if not (i + 2 >= len(math_expr)):
                    n_ch = math_expr[i + 2]
                    if math_expr[i + 1] == " " and (
                            issubclass(self.get_type(n_ch), Digit) or issubclass(self.get_type(n_ch), MathExpr)):
                        raise TooManySpaces()

            elif issubclass(t, Operator):
                if ch == "*" or ch == "/":
                    if not (i + 2 >= len(math_expr)):
                        n_ch = math_expr[i + 2]
                        if math_expr[i + 1] == " " and n_ch == ch:
                            raise TooManySpaces()
                elif ch == "<" or ch == ">" or ch == "=":
                    if not (i + 2 >= len(math_expr)):
                        n_ch = math_expr[i + 2]
                        if math_expr[i + 1] == " " and (n_ch == "<" or n_ch == ">" or n_ch == "="):
                            raise TooManySpaces()

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
        add_multiply = False
        for symbol in self.math_expr[1:]:
            next_type = self.get_type(symbol)
            if issubclass(next_type, Scope):
                if issubclass(sym_type, Digit) and issubclass(next_type, OpenScope):
                    add_multiply = True
            elif issubclass(next_type, Digit) and issubclass(sym_type, CloseScope):
                add_multiply = True
            elif symbol == "." and issubclass(sym_type, Digit) or issubclass(next_type, Digit) and lexem[-1] == ".":
                lexem += symbol
                continue
            elif issubclass(sym_type, MathExpr) and issubclass(next_type, Digit):
                lexem += symbol
                continue
            elif sym_type == next_type:
                if issubclass(sym_type, Operator):
                    if lexem in available_operations:
                        if lexem + symbol in available_operations:
                            lexem += symbol
                        else:
                            lexems.append(lexem)
                            lexem = symbol
                            continue
                    elif len(lexem) >= 1 and lexem not in available_operations:
                        if lexem + symbol in available_operations:
                            lexem += symbol
                        else:
                            lexems.append(lexem)
                            lexem = symbol
                    continue
                lexem += symbol
                continue
            lexems.append(lexem)
            if add_multiply:
                lexems.append("*")
                add_multiply = False
            sym_type = next_type
            lexem = symbol
        lexems.append(lexem)

        is_changed, lexems = self.change_signs(lexems)
        while is_changed:
            is_changed, lexems = self.change_signs(lexems)
        return lexems

    def check_lexems(self, lexems):
        len_lexems = len(lexems)
        i = 0
        while i < len_lexems:
            lexem = lexems[i]
            if lexem in available_operations:
                i += 1
                yield lexem

            elif lexem in available_functions:
                if lexems[i + 1] not in available_order_symbols:
                    raise UnrecognizedFunc()
                arguments, pos = self.get_argument_for_function(lexems[i + 2:])
                func = available_functions[lexem]
                try:
                    result = func(*arguments)
                    i += pos + 2
                    yield result
                except TypeError:
                    raise TooManyArguments()
            elif lexem in available_constants:
                yield available_constants[lexem]
                i += 1
            elif lexem in available_order_symbols:
                if lexem == "(" or lexem == ")":
                    i += 1
                    yield lexem
            else:
                try:
                    num = float(lexem)
                    int_num = int(num)
                    if int_num == num:
                        num = int_num
                except ValueError:
                    raise UnrecognizedLexem(lexem)
                i += 1
                yield num

    def get_argument_for_function(self, lexems):
        arguments = []
        sub_expression = []
        amount_of_scopes = 0
        amount_of_funcs = 0
        i = 0
        for lexem in lexems:
            if lexem == ",":
                i += 1
                if not amount_of_funcs:
                    argument = ExpressionCalculator.calc(
                        ExpressionCalculator.shunting_yard(self.check_lexems(sub_expression)), args=True)
                    arguments.append(argument)
                    sub_expression = []
                    continue
                sub_expression.append(lexem)
            elif lexem in available_functions:
                amount_of_funcs += 1
                sub_expression.append(lexem)
                i += 1
            elif lexem == ")":
                i += 1
                if not amount_of_scopes:
                    break
                if amount_of_funcs and amount_of_scopes:
                    amount_of_funcs -= 1
                amount_of_scopes -= 1
                sub_expression.append(lexem)
            elif lexem == "(":
                sub_expression.append(lexem)
                amount_of_scopes += 1
                i += 1
            else:
                sub_expression.append(lexem)
                i += 1

        if sub_expression:
            argument = ExpressionCalculator.calc(ExpressionCalculator.shunting_yard(self.check_lexems(sub_expression)),
                                                 args=True)
            if isinstance(argument, list):
                arguments.extend(argument)
            else:
                arguments.append(argument)
        if amount_of_scopes:
            raise TooManyBrackets()
        return arguments, i

    def change_sign(self, lexem, lexems, index):
        prev_lexem = lexems[index - 1]
        is_changed = False
        if index == 0 or (
                (prev_lexem in available_operations or prev_lexem in ["(", ")"]) and prev_lexem != ")"):
            lexems[index] = lexem + " "
            is_changed = True
        return is_changed

    def change_signs(self, lexems):
        is_changed = False
        for i in range(len(lexems) - 1):
            lexem = lexems[i]
            next_lexem = lexems[i + 1]
            if lexem in available_operations and lexem in ["-", "+"]:
                is_dig = False
                try:
                    _ = float(next_lexem)
                    is_dig = True
                except ValueError:
                    pass
                if is_dig:
                    is_changed = self.change_sign(lexem, lexems, i)
                elif next_lexem in available_operations and next_lexem in ["(", "- ", "+ "]:
                    is_changed = self.change_sign(lexem, lexems, i)
                elif is_dig or next_lexem in available_constants:
                    is_changed = self.change_sign(lexem, lexems, i)
                elif next_lexem in available_functions:
                    is_changed = self.change_sign(lexem, lexems, i)

        return is_changed, lexems


def calculation(expr):
    math_expr = MathExpressionParser(expr)
    expr = math_expr.to_lexems()
    return ExpressionCalculator.calc(ExpressionCalculator.shunting_yard(math_expr.check_lexems(expr)))


if __name__ == "__main__":
    math_expr = MathExpressionParser(".1 * 2.0**56.0")
    print(math_expr.to_lexems())
