def main():
    import argparse

    from pycalc.core.calculator import calculate

    def parse_arguments():
        parser = argparse.ArgumentParser(description='Pure-python command-line calculator.')

        parser.add_argument('expression', type=str, help='Mathematics expression')
        parser.add_argument("-m", '--module', nargs="+", default=[], help="module_name")

        args = parser.parse_args()
        return args.expression, args.module

    expression, module_names = parse_arguments()
    result = calculate(expression, module_names)
    return result


if __name__ == "__main__":
    print(main())
