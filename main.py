import inspect

from console_app.parser import ArgumentParser
from core.recognizer import calculation
from core.operatios import available_functions, available_constants

if __name__ == "__main__":
    math_expr, module = ArgumentParser.parse_arguments()
    if module:
        module = __import__(module)
        available_functions_names_of_module = filter(lambda x: not x.startswith("_"), dir(module))
        for avai_name in available_functions_names_of_module:
            obj = getattr(module, avai_name)
            if inspect.isfunction(obj) or inspect.isbuiltin(obj):
                available_functions.update({avai_name: obj})
            if isinstance(obj, int) or isinstance(obj, float):
                available_constants.update({avai_name: obj})
    print(calculation(math_expr))