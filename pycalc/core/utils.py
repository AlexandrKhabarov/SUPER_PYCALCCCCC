import inspect

from pycalc.core.exceptions import ModuleNotFound


def add_available_names_from_module(available_functions, available_constants, module_name):
    try:
        module = __import__(module_name)
        available_functions_names_of_module = filter(lambda x: not x.startswith("_"), dir(module))
        for available_name in available_functions_names_of_module:
            obj = getattr(module, available_name)
            if inspect.isfunction(obj) or inspect.isbuiltin(obj):
                available_functions.update({available_name: obj})
            if isinstance(obj, int) or isinstance(obj, float):
                available_constants.update({available_name: obj})
    except ModuleNotFoundError:
        raise ModuleNotFound()
