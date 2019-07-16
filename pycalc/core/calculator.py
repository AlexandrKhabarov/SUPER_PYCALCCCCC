from pycalc.core.expressions import Interpreter
from pycalc.core.parser import Parser
from pycalc.core.scanner import Scanner


def calculate(source, modules=None):
    assert isinstance(modules, (list, type(None)))

    scanner = Scanner(source)
    tokens = scanner.get_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    interpreter = Interpreter()

    if modules is not None:
        interpreter.globals.update(modules)

    result = interpreter.evaluate(tree)
    return result
