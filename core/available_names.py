from core.utils import add_available_names_from_module

available_functions = {}
available_constants = {}

add_available_names_from_module(available_functions, available_constants, "math")
add_available_names_from_module(available_functions, available_constants, "builtins")
