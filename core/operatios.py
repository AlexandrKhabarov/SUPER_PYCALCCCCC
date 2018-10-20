available_operations = {
    "+": (1, lambda x, y: x + y, "Right"),
    "-": (1, lambda x, y: x - y, "Right"),
    "+ ": (3, lambda x: +x, "Left"),
    "- ": (3, lambda x: -x, "Left"),
    "*": (2, lambda x, y: x * y, "Right"),
    "//": (2, lambda x, y: x // y, "Right"),
    "**": (3, lambda x, y: x ** y, "Left"),
    "%": (2, lambda x, y: x % y, "Right"),
    "^": (3, lambda x, y: x ** y, "Left"),
    "<": (0, lambda x, y: x < y, "Right"),
    ">": (0, lambda x, y: x > y, "Right"),
    "<=": (0, lambda x, y: x <= y, "Right"),
    ">=": (0, lambda x, y: x >= y, "Right"),
    "==": (0, lambda x, y: x >= y, "Right"),
    "!=": (0, lambda x, y: x != y, "Right"),
    "/": (2, lambda x, y: x / y, "Right"),
}
available_order_symbols = {"(", ")"}