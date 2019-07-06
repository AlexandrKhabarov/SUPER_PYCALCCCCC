class Token:
    def __init__(self, type_, lexeme, literal, pos):
        self.type_ = type_
        self.lexeme = lexeme
        self.literal = literal
        self.pos = pos

    def __str__(self):
        return f"{self.type_} {self.lexeme} {self.literal}"

    __repr__ = __str__
