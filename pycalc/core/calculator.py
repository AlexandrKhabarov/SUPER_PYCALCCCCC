from pycalc.core.expressions import Interpreter
from pycalc.core.parser import Parser
from pycalc.core.scanner import Scanner


def calculate(source, module_names=None):
    assert isinstance(module_names, (list, type(None)))

    scanner = Scanner(source)
    tokens = scanner.get_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    interpreter = Interpreter()

    if module_names is not None:
        interpreter.globals.update(module_names)

    result = interpreter.evaluate(tree)
    return result
