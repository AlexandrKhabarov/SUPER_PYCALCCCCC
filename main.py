from console_app.parser import ArgumentParser
from core.available_names import available_functions, available_constants
from core.recognizer import calculation
from core.utils import add_available_names_from_module

if __name__ == "__main__":
    math_expr, module_name = ArgumentParser.parse_arguments()
    if module_name:
        add_available_names_from_module(available_functions, available_constants, module_name)
    print(calculation(math_expr))
