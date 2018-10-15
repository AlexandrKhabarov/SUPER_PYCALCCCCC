from core.operatios import available_functions, available_operations, available_order_symbols, available_constants


# TODO add support of spaces between characters and unary "-" for expressions
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
    def calc(cls, polish, args=False):
        stack = []
        for token in polish:
            if token in available_operations:
                y, x = stack.pop(), stack.pop()
                stack.append(available_operations[token][1](x, y))
            else:
                stack.append(float(token))
        if not args and len(stack) > 1:
            raise Exception("Didn 't find operator")
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
                        raise Exception("Too many spaces")

            elif issubclass(t, Operator):
                if ch == "*" or ch == "/":
                    if not (i + 2 >= len(math_expr)):
                        n_ch = math_expr[i + 2]
                        if math_expr[i + 1] == " " and n_ch == ch:
                            raise Exception("Too many space")
                elif ch == "<" or ch == ">" or ch == "=":
                    if not (i + 2 >= len(math_expr)):
                        n_ch = math_expr[i + 2]
                        if math_expr[i + 1] == " " and (n_ch == "<" or n_ch == ">" or n_ch == "="):
                            raise Exception("Too many spaces")

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
            elif sym_type == next_type:
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
                    raise ValueError("Can't solve function")
                arguments, pos = self.get_argument_for_function(lexems[i + 2:])
                func = available_functions[lexem]
                try:
                    result = func(*arguments)
                    i += pos + 2
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
        i = 0
        for lexem in lexems:
            if lexem == ",":
                i += 1
                if not function:
                    argument = Expression.calc(Expression.shunting_yard(self.check_lexems(sub_expression)), args=True)
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
            argument = Expression.calc(Expression.shunting_yard(self.check_lexems(sub_expression)), args=True)
            if isinstance(argument, list):
                arguments.extend(argument)
            else:
                arguments.append(argument)
        if scopes:
            raise SyntaxError("Forgot closed scope")
        return arguments, i

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
                except Exception:
                    pass
                if is_dig:
                    prev_lexem = lexems[i - 1]
                    is_changed = False
                    if i == 0 or (
                            (prev_lexem in available_operations or prev_lexem in ["(", ")"]) and prev_lexem != ")"):
                        lexems[i] = lexem + " "
                        is_changed = True
                elif next_lexem in available_operations and next_lexem in ["(", "- ", "+ "]:
                    prev_lexem = lexems[i - 1]
                    is_changed = False
                    if i == 0 or (
                            (prev_lexem in available_operations or prev_lexem in ["(", ")"]) and prev_lexem != ")"):
                        lexems[i] = lexem + " "
                        is_changed = True
                elif is_dig or next_lexem in available_constants:
                    prev_lexem = lexems[i - 1]
                    is_changed = False
                    if i == 0 or (
                            (prev_lexem in available_operations or prev_lexem in ["(", ")"]) and prev_lexem != ")"):
                        lexems[i] = lexem + " "
                        is_changed = True
                elif next_lexem in available_functions:
                    prev_lexem = lexems[i - 1]
                    is_changed = False
                    if i == 0 or (
                            (prev_lexem in available_operations or prev_lexem in ["(", ")"]) and prev_lexem != ")"):
                        lexems[i] = lexem + " "
                        is_changed = True

        return is_changed, lexems


def calculation(expr):
    math_expr = MathExpression(expr)
    expr = math_expr.to_lexems()
    return Expression.calc(Expression.shunting_yard(math_expr.check_lexems(expr)))


if __name__ == "__main__":
    math_expr = MathExpression("-13")
    print(math_expr.to_lexems())
    math_expr = MathExpression("6-(-13)")
    print(math_expr.to_lexems())
    math_expr = MathExpression("1---1")
    print(math_expr.to_lexems())
    math_expr = MathExpression("-+---+-1")
    print(math_expr.to_lexems())
