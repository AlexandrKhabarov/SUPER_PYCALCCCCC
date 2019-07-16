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

    def update(self, modules):
        pass
