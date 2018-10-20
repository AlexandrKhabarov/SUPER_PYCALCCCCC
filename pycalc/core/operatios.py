class Operation:
    def __init__(self, priority, func, is_right_associated):
        self.priority = priority
        self.func = func
        self.is_right_associated = is_right_associated
        self.co_arguments = self.func.__code__.co_argcount


available_operations = {
    "+": Operation(1, lambda x, y: x + y, True),
    "-": Operation(1, lambda x, y: x - y, True),
    "+ ": Operation(3, lambda x: +x, False),
    "- ": Operation(3, lambda x: -x, False),
    "*": Operation(2, lambda x, y: x * y, True),
    "//": Operation(2, lambda x, y: x // y, True),
    "**": Operation(3, lambda x, y: x ** y, False),
    "%": Operation(2, lambda x, y: x % y, True),
    "^": Operation(3, lambda x, y: x ** y, False),
    "<": Operation(0, lambda x, y: x < y, True),
    ">": Operation(0, lambda x, y: x > y, True),
    "<=": Operation(0, lambda x, y: x <= y, True),
    ">=": Operation(0, lambda x, y: x >= y, True),
    "==": Operation(0, lambda x, y: x >= y, True),
    "!=": Operation(0, lambda x, y: x != y, True),
    "/": Operation(2, lambda x, y: x / y, True),
}
available_order_symbols = {"(", ")"}
