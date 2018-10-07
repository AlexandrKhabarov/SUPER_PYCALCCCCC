available_operations = {
    "+": (1, lambda x, y: x + y),
    "-": (1, lambda x, y: x - y),
    "*": (2, lambda x, y: x * y),
    "//": (2, lambda x, y: x // y),
    "**": (3, lambda x, y: x ** y),
    "^": (3, lambda x, y: x ** y),
    "<": (0, lambda x, y: x < y),
    ">": (0, lambda x, y: x > y),
    "<=": (0, lambda x, y: x <= y),
    ">=": (0, lambda x, y: x >= y),
    "/": (2, lambda x, y: x / y),
}

available_functions = {}

module = __import__("math")
builtins = __import__("builtins")


class Function:
    def __init__(self, func: callable):
        self.func = func
        self._amount_of_arguments = None

    @property
    def amount_of_arguments(self):
        if self.amount_of_arguments is None:
            self._amount_of_arguments = self.func.__code__.co_arguments
        return self.amount_of_arguments


available_functions_names_of_module = filter(lambda x: not x.startswith("_"), dir(module))
for avai_name in available_functions_names_of_module:
    available_functions.update({avai_name: getattr(module, avai_name)})

for avai_name in filter(lambda x: not x.startswith("_"), dir(builtins)):
    available_functions.update({avai_name: getattr(builtins, avai_name)})

available_order_symbols = {"(", ")"}

AVAILABLE_SYMBOLS = {}
