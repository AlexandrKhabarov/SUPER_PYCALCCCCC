from pycalc.core.errors import parser_error
from pycalc.core.expressions import Binary, Literal, Grouping, Unary, Call
from pycalc.core.token_types import TokenTypes


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self._current = 0

    def parse(self):
        try:
            return self.expression()
        except Exception as e:
            print(e)
            pass

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while self.match(TokenTypes.BANG_EQUAL, TokenTypes.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.addition()

        while self.match(TokenTypes.GREATER, TokenTypes.GREATER_EQUAL, TokenTypes.LESS, TokenTypes.LESS_EQUAL):
            operator = self.previous()
            right = self.addition()
            expr = Binary(expr, operator, right)

        return expr

    def addition(self):
        expr = self.multiplication()

        while self.match(TokenTypes.PLUS, TokenTypes.MINUS):
            operator = self.previous()
            right = self.multiplication()
            expr = Binary(expr, operator, right)
        return expr

    def multiplication(self):
        expr = self.unary()

        while self.match(TokenTypes.SLASH,
                         TokenTypes.STAR,
                         TokenTypes.SLASH_SLASH,
                         TokenTypes.PERCENTS,
                         TokenTypes.CAP,
                         TokenTypes.STAR_STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenTypes.BANG, TokenTypes.MINUS, TokenTypes.PLUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.call()

    def call(self):
        expr = self.primary()

        while True:
            if self.match(TokenTypes.LEFT_PAREN):
                expr = self.find_call(expr)
            else:
                break

        return expr

    def primary(self):
        if self.match(TokenTypes.NUMBER):
            return Literal(self.previous().literal)
        elif self.match(TokenTypes.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenTypes.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        parser_error(self.peek(), "Expect Expression.")

    def find_call(self, callable_):
        arguments = []
        if not self.check(TokenTypes.RIGHT_PAREN):
            while self.match(TokenTypes.COMMA):
                arguments.append(self.expression())

        paren = self.consume(TokenTypes.RIGHT_PAREN, "Expect ')' after arguments.")

        return Call(callable_, paren, arguments)

    def match(self, *types):
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def consume(self, type_, err_msg):
        if self.check(type_):
            return self.advance()
        parser_error(self.peek(), err_msg)

    def check(self, type_):
        if self.is_end():
            return False
        return self.peek().type_ == type_

    def advance(self):
        if not self.is_end():
            self._current += 1

        return self.previous()

    def is_end(self):
        return self.peek().type_ == TokenTypes.EOF

    def peek(self):
        return self.tokens[self._current]

    def previous(self):
        return self.tokens[self._current - 1]
