from core.operatios import available_functions, available_operations, available_order_symbols, available_constants


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
        return stack[0] if len(stack) == 1 else stack

    @classmethod
    def shunting_yard(cls, parsed_formula):
        stack = []
        opened_scope = 0
        closed_scope = 0
        for token in parsed_formula:
            if token in available_operations:
                while stack and stack[-1] != "(" and available_operations[token][0] <= available_operations[stack[-1]][
                    0]:
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
            raise SyntaxError("Too many Scopes")
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
        add_multiply = False
        for symbol in self.math_expr[1:]:
            next_type = self.get_type(symbol)
            if issubclass(next_type, Scope):
                if issubclass(sym_type, Digit) and issubclass(next_type, OpenScope):
                    add_multiply = True
            elif symbol == "." and issubclass(sym_type, Digit) or issubclass(next_type, Digit) and lexem[-1] == ".":
                lexem += symbol
                continue
            elif sym_type == next_type:
                lexem += symbol
                continue
            lexems.append(lexem)
            if add_multiply:
                lexems.append("*")
                add_multiply=False
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
                except ValueError:
                    raise TypeError(f"lexem {lexem} is not recognized")
                i += 1
                yield num


    def get_argument_for_function(self, lexems):
        arguments = []
        sub_expression = []
        scopes = 0
        function = 0
        i = 1
        for lexem in lexems:
            if lexem == ",":
                i += 1
                if not function:
                    argument = Expression.calc(Expression.shunting_yard(self.check_lexems(sub_expression)))
                    arguments.append(argument)
                    sub_expression = []
                    continue
                sub_expression.append(lexem)
            elif lexem in available_functions:
                function += 1
                sub_expression.append(lexem)
                i += 1
            elif lexem == ")":
                i += 1
                if not scopes:
                    break
                if function and scopes:
                    function -= 1
                scopes -= 1
                sub_expression.append(lexem)
            elif lexem == "(":
                sub_expression.append(lexem)
                scopes += 1
                i += 1
            else:
                sub_expression.append(lexem)
                i += 1

        if sub_expression:
            argument = Expression.calc(Expression.shunting_yard(self.check_lexems(sub_expression)))
            if isinstance(argument, list):
                arguments.extend(argument)
            else:
                arguments.append(argument)
        if scopes:
            raise SyntaxError("Forgot closed scope")
        return arguments, i

def calculation(expr):
    math_expr = MathExpression(expr)
    expr = math_expr.to_lexems()
    return Expression.calc(Expression.shunting_yard(math_expr.check_lexems(expr)))

if __name__ == "__main__":
    print(calculation("1+1"))