import inspect

from pycalc.core.errors import ModuleNotFound


def add_available_names_from_module(available_functions, available_constants, module_name):
    try:
        module = __import__(module_name)
        available_functions_names_of_module = filter(lambda x: not x.startswith("_"), dir(module))
        for available_name in available_functions_names_of_module:
            obj = getattr(module, available_name)
            if _is_func(obj):
                _add_to_the_namespace(available_functions, available_name, obj, prefix="Function")
            elif _is_const(obj):
                _add_to_the_namespace(available_constants, available_name, obj, prefix="Const")
    except ModuleNotFoundError:
        raise ModuleNotFound()


def _is_const(obj):
    return isinstance(obj, int) or isinstance(obj, float)


def _is_func(obj):
    return callable(obj) or inspect.isbuiltin(obj)


def _add_to_the_namespace(namespace, available_name, obj, silent=True, prefix='Obj'):
    if available_name in namespace and not silent:
        print(f"{prefix} with name: {available_name} already exist in namespace.")
    namespace.update({available_name: obj})
