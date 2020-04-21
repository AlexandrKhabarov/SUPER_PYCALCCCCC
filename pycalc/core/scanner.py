from pycalc.core.errors import error
from pycalc.core.token_types import TokenTypes
from pycalc.core.tokens import Token


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []

        self._start = 0
        self._current = 0

    def get_tokens(self):
        self._scan_tokens()
        return self.tokens

    def _scan_tokens(self):
        while not self.is_end:
            self._start = self._current
            self._scan_token()
        eof = Token(TokenTypes.EOF, "", None, self._start)
        self.tokens.append(eof)

    @property
    def is_end(self):
        return self._current >= len(self.source)

    def _scan_token(self):
        c = self._advance()
        if c == "(":
            self._add_token(TokenTypes.LEFT_PAREN)
        elif c == ")":
            self._add_token(TokenTypes.RIGHT_PAREN)
        elif c == ",":
            self._add_token(TokenTypes.COMMA)
        elif c == "-":
            self._add_token(TokenTypes.MINUS)
        elif c == "+":
            self._add_token(TokenTypes.PLUS)
        elif c == ";":
            self._add_token(TokenTypes.SEMICOLON)
        elif c == "^":
            self._add_token(TokenTypes.CAP)
        elif c == "%":
            self._add_token(TokenTypes.PERCENTS)
        elif c == "*":
            type_ = TokenTypes.STAR_STAR if self._match("*") else TokenTypes.STAR
            self._add_token(type_)
        elif c == "!":
            type_ = TokenTypes.NOT_EQUAL if self._match("=") else TokenTypes.NOT
            self._add_token(type_)
        elif c == "=":
            type_ = TokenTypes.EQUAL_EQUAL if self._match("=") else TokenTypes.EQUAL
            self._add_token(type_)
        elif c == "<":
            type_ = TokenTypes.LESS_EQUAL if self._match("=") else TokenTypes.LESS
            self._add_token(type_)
        elif c == ">":
            type_ = TokenTypes.GREATER if self._match("=") else TokenTypes.GREATER_EQUAL
            self._add_token(type_)
        elif c == "/":
            type_ = TokenTypes.SLASH_SLASH if self._match("/") else TokenTypes.SLASH
            self._add_token(type_)
        elif c == " " or c == "\r" or c == "\t":
            pass
        else:
            if (c == "." and self._is_digit(self._peek())) or self._is_digit(c):
                self._number()
            elif self._is_alpha(c):
                self._identifier()
            else:
                error(self._current, "Unexpected Character")

    def _advance(self):
        self._current += 1
        return self.source[self._current - 1]

    def _add_token(self, type_, literal=None):
        text = self.source[self._start: self._current]
        token = Token(type_, text, literal, self._start)
        self.tokens.append(token)

    def _match(self, expected):
        if self.is_end:
            return False
        if self.source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _peek(self):
        if self.is_end:
            return "\0"
        return self.source[self._current]

    def _is_digit(self, c):
        return c.isdigit()

    def _number(self):
        while self._is_digit(self._peek()):
            self._advance()

        if self._peek() == "." and self._is_digit(self._peek_next()):
            self._advance()

            while self._is_digit(self._peek()):
                self._advance()

        text = self.source[self._start: self._current]
        type_ = float if "." in text else int
        return self._add_token(TokenTypes.NUMBER, type_(self.source[self._start: self._current]))

    def _peek_next(self):
        if self._current + 1 > len(self.source):
            return "\0"
        return self.source[self._current + 1]

    def _is_alpha(self, c):
        return c.isalpha() or c == "_"

    def _identifier(self):
        while self._is_alpha_numeric(self._peek()):
            self._advance()
        type_ = TokenTypes.IDENTIFIERS
        return self._add_token(type_)

    def _is_alpha_numeric(self, c):
        return self._is_alpha(c) or self._is_digit(c)
