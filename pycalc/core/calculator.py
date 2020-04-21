from pycalc.core.expressions import Interpreter
from pycalc.core.parser import Parser
from pycalc.core.scanner import Scanner


def calculate(source, external_module_names=None):
    assert isinstance(external_module_names, (list, type(None)))

    scanner = Scanner(source)
    tokens = scanner.get_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    interpreter = Interpreter()

    if external_module_names is not None:
        interpreter.globals.bulk_update(external_module_names)

    result = interpreter.evaluate(tree)
    return result
