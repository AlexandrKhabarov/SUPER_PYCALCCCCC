from pycalc.core.errors import runtime_error


class Environment:
    def __init__(self):
        self.map = {}

    def define(self, name, value):
        self.map[name] = value

    def get(self, name):
        try:
            return self.map[name.lexem]
        except KeyError:
            runtime_error(name, f"Undefined variable '{name.lexeme}'.")
