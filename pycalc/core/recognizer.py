from pycalc.core.exceptions import TooManySpaces, TooManyBrackets, TooManyArguments, UnrecognizedOperator, \
    UnrecognizedLexem, UnrecognizedFunc, NotEnoughArguments, EmptyExpression
from pycalc.core.operatios import available_operations, available_order_symbols
from pycalc.core.types import Digit, Operator, MathExpr, Bracket, OpenBracket, CloseBracket


class ExpressionCalculator:
    @classmethod
    def calc(cls, polish):
        stack = []
        for token in polish:
            if token in available_operations:
                operation = available_operations[token]
                try:
                    if operation.co_arguments == 2:
                        y, x = stack.pop(), stack.pop()
                        stack.append(operation.func(x, y))
                    elif operation.co_arguments == 1:
                        y = stack.pop()
                        stack.append(operation.func(y))
                except IndexError:
                    raise NotEnoughArguments()
            else:
                stack.append(token)
        if len(stack) > 1:
            raise UnrecognizedOperator()
        return stack[0] if len(stack) == 1 else stack

    @classmethod
    def pops_token_in_right_order(cls, parsed_formula):
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
    def __init__(self, expression, funcs, consts):
        self.funcs = funcs
        self.consts = consts
        if not expression:
            raise EmptyExpression()
        self.check_spaces(expression)
        self.expression = expression.replace(" ", "")

    def check_spaces(self, expression):
        for i, ch in enumerate(expression):
            t = self.get_type(ch)
            if isinstance(t, Digit) or isinstance(t, MathExpr):
                if not (i + 2 >= len(expression)):
                    n_ch = expression[i + 2]
                    if expression[i + 1] == " " and (
                            isinstance(self.get_type(n_ch), Digit) or isinstance(self.get_type(n_ch), MathExpr)):
                        raise TooManySpaces()

            elif isinstance(t, Operator):
                if ch == "*" or ch == "/":
                    if not (i + 2 >= len(expression)):
                        n_ch = expression[i + 2]
                        if expression[i + 1] == " " and n_ch == ch:
                            raise TooManySpaces()
                elif ch == "<" or ch == ">" or ch == "=":
                    if not (i + 2 >= len(expression)):
                        n_ch = expression[i + 2]
                        if expression[i + 1] == " " and (n_ch == "<" or n_ch == ">" or n_ch == "="):
                            raise TooManySpaces()

    def get_type(self, symbol):
        if symbol.isdigit():
            sym_type = Digit()
        elif symbol == "(":
            sym_type = OpenBracket()
        elif symbol == ")":
            sym_type = CloseBracket()
        elif symbol.isalpha():
            sym_type = MathExpr()
        else:
            sym_type = Operator()
        return sym_type

    def to_lexems(self):
        sym_type = self.get_type(self.expression[0])
        lexem = self.expression[0]
        lexems = []
        add_multiply = False
        for symbol in self.expression[1:]:
            next_type = self.get_type(symbol)
            if isinstance(next_type, Bracket):
                if isinstance(sym_type, Digit) and isinstance(next_type, OpenBracket):
                    add_multiply = True
            elif isinstance(next_type, Digit) and isinstance(sym_type, CloseBracket):
                add_multiply = True
            elif symbol == "." and isinstance(sym_type, Digit) or isinstance(next_type, Digit) and lexem[-1] == ".":
                lexem += symbol
                continue
            elif isinstance(sym_type, MathExpr) and isinstance(next_type, Digit):
                lexem += symbol
                continue
            elif sym_type == next_type:
                if isinstance(sym_type, Operator):
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

            elif lexem in self.funcs:
                if lexems[i + 1] not in available_order_symbols:
                    raise UnrecognizedFunc()
                arguments, pos = self.get_argument_for_function(lexems[i + 2:])
                func = self.funcs[lexem]
                try:
                    result = func(*arguments)
                    i += pos + 2
                    yield result
                except TypeError:
                    raise TooManyArguments()
            elif lexem in self.consts:
                yield self.consts[lexem]
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
        amount_of_scopes = 1
        amount_of_funcs = 0
        i = 0
        for lexem in lexems:
            if lexem == ",":
                i += 1
                if not amount_of_funcs:
                    argument = ExpressionCalculator.calc(
                        ExpressionCalculator.pops_token_in_right_order(self.check_lexems(sub_expression)))
                    arguments.append(argument)
                    sub_expression = []
                    continue
                sub_expression.append(lexem)
            elif lexem in self.funcs:
                amount_of_funcs += 1
                sub_expression.append(lexem)
                i += 1
            elif lexem == ")":
                i += 1
                amount_of_scopes -= 1
                if not amount_of_scopes:
                    break
                if amount_of_funcs and amount_of_scopes:
                    amount_of_funcs -= 1
                sub_expression.append(lexem)
            elif lexem == "(":
                sub_expression.append(lexem)
                amount_of_scopes += 1
                i += 1
            else:
                sub_expression.append(lexem)
                i += 1

        if sub_expression:
            argument = ExpressionCalculator.calc(
                ExpressionCalculator.pops_token_in_right_order(self.check_lexems(sub_expression)))
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
                elif is_dig or next_lexem in self.consts:
                    is_changed = self.change_sign(lexem, lexems, i)
                elif next_lexem in self.funcs:
                    is_changed = self.change_sign(lexem, lexems, i)

        return is_changed, lexems


def calculation(expr, funcs, consts):
    math_expr = MathExpressionParser(expr, funcs, consts)
    expr = math_expr.to_lexems()
    return ExpressionCalculator.calc(ExpressionCalculator.pops_token_in_right_order(math_expr.check_lexems(expr)))
