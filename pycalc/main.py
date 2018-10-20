from pycalc.console_app.parser import ArgumentParser
from pycalc.core.available_names import available_functions, available_constants
from pycalc.core.recognizer import calculation
from pycalc.core.utils import add_available_names_from_module


def main():
    math_expr, module_names = ArgumentParser.parse_arguments()
    for module_name in module_names:
        add_available_names_from_module(available_functions, available_constants, module_name)
    try:
        print(calculation(math_expr))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
