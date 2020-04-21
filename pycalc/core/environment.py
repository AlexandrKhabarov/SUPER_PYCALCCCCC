import importlib

from pycalc.core.errors import runtime_error


class Environment:
    def __init__(self):
        self._map = {}
        self.bulk_update(["math", "builtins"])

    def bulk_update(self, module_names):
        for module_name in module_names:
            self.update(module_name)

    def update(self, module_name):
        module = importlib.import_module(module_name)
        for obj_name in module.__dict__.keys():
            if not obj_name.startswith("_"):
                obj = getattr(module, obj_name)
                if callable(obj):
                    obj = create_callable(obj)
                self.define(obj_name, obj)

    def define(self, name, value):
        self._map[name] = value

    def get(self, name):
        try:
            return self._map[name.lexeme]
        except KeyError:
            runtime_error(name, f"Undefined variable '{name.lexeme}'.")


class Callable:
    def call(self, arguments):
        pass


def create_callable(callable_obj):
    def call(self, arguments):
        return callable_obj(*arguments)

    callee = Callable()

    method = call.__get__(callee, Callable)
    callee.call = method

    return callee
