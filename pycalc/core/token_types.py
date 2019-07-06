from enum import Enum, auto


class TokenTypes(Enum):
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SLASH = auto()
    SLASH_SLASH = auto()
    PERCENTS = auto()
    CAP = auto()
    STAR = auto()
    STAR_STAR = auto()

    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    NUMBER = auto()
    IDENTIFIERS = auto()
