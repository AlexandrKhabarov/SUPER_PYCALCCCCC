from pycalc.core.expressions import Interpreter
from pycalc.core.parser import Parser
from pycalc.core.scanner import Scanner


def calculate(source):
    scanner = Scanner(source)
    tokens = scanner.get_tokens()
    parser = Parser(tokens)
    tree = parser.parse()
    interpreter = Interpreter()
    result = interpreter.evaluate(tree)
    return result
