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
    @classmethod
    def calc(cls, polish):
        stack = []
        for token in polish:
            if token in available_operations:
                y, x = stack.pop(), stack.pop()
                stack.append(available_operations[token][1](x, y))
            else:
                stack.append(float(token))
        return stack[0]

    @classmethod
    def shunting_yard(cls, parsed_formula):
        stack = []
        for token in parsed_formula:
            if token in available_operations:
                while stack and stack[-1] != "(" and available_operations[token][0] <= available_operations[stack[-1]][
                    0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()


class MathExpression:
    def __init__(self, math_expr, rules=None):
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
                    raise ValueError("Can't solve function")
                arguments, pos = self.get_argument_for_function(lexems[i + 2:])
                func = available_functions[lexem]
                try:
                    result = func(*arguments)
                    i += pos + 3
                    yield result
                except TypeError:
                    raise Exception("Too many arguments")

            elif lexem in available_order_symbols:
                if lexem == "(" or lexem == ")":
                    i += 1
                    yield lexem
            else:
                try:
                    try:
                        num = float(lexem)
                    except ValueError:
                        num = int(lexem)
                    i += 1
                    yield num
                except ValueError:
                    raise TypeError(f"lexem {lexem} is not recognized")

    def get_argument_for_function(self, lexems):
        arguments = []
        sub_expression = []
        i = 0
        for lexem in lexems:
            if lexem == ",":
                argument = list(self.check_lexems(sub_expression))
                arguments.extend(argument)
                sub_expression = []
                continue
            elif lexem == ")":
                argument = list(self.check_lexems(sub_expression))
                arguments.extend(argument)
                return arguments, i + 1
            else:
                sub_expression.append(lexem)
            i += 1

        argument = list(self.check_lexems(sub_expression))
        arguments.extend(argument)
        return arguments, 1


if __name__ == "__main__":
    math_expr = MathExpression("1+2**2*2*max(1, 1+1+1, 3)*1")
    expr = math_expr.to_lexems()
    print(Expression.calc(Expression.shunting_yard(math_expr.check_lexems(expr))))
