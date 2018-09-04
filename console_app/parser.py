import argparse

class ArgumentParser:

    @classmethod
    def parse_arguments(cls):
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('math_expr', type=str, help='mathematic expression')
        parser.add_argument("-m", '--module', type=str, help="module_name")

        args = parser.parse_args()
        return args.math_expr, args.module

