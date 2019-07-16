import argparse

from pycalc.core.calculator import calculate


class ArgumentParser:

    @classmethod
    def parse_arguments(cls):
        parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')
        parser.add_argument('expression', type=str, help='Mathematics expression')
        parser.add_argument("-m", '--module', nargs="+", default=[], help="module_name")

        args = parser.parse_args()
        return args.expression, args.module


def main():
    expression, module_names = ArgumentParser.parse_arguments()
    result = calculate(expression)
    return result


if __name__ == "__main__":
    print(main())
