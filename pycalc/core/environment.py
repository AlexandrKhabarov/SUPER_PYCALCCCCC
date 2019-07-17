import importlib

from pycalc.core.errors import runtime_error


class Environment:
    def __init__(self):
        self.map = {}
        self.update(["math", "builtins"])

    def define(self, name, value):
        self.map[name] = value

    def get(self, name):
        try:
            return self.map[name.lexeme]
        except KeyError:
            runtime_error(name, f"Undefined variable '{name.lexeme}'.")

    def update(self, names):
        for name in names:
            module = importlib.import_module(name)
            for name in filter(lambda name: not name.startswith("_"), module.__dict__.keys()):
                obj = getattr(module, name)
                if callable(obj):
                    obj = create_callable(obj)
                self.define(name, obj)


class Callable():

    def call(self, arguments):
        pass


def create_callable(callable_):
    def call(self, arguments):
        return callable_(*arguments)

    callee = Callable()

    method = call.__get__(callee, Callable)
    callee.call = method

    return callee
