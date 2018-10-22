class ErrorMessageFormatter(type):
    MESSAGE_ATTR = "ERROR_MESSAGE"

    def __new__(mcs, class_name, parents, attributes):
        error_message = attributes.get(mcs.MESSAGE_ATTR, None)
        if error_message:
            attributes[mcs.MESSAGE_ATTR] = f"ERROR: {error_message}"
        cls = super().__new__(mcs, class_name, parents, attributes)
        return cls

    def __call__(cls, *args, **kwargs):
        return super().__call__(getattr(cls, cls.MESSAGE_ATTR))


class CustomSyntaxError(SyntaxError, metaclass=ErrorMessageFormatter):
    pass


class CustomValueError(ValueError, metaclass=ErrorMessageFormatter):
    pass


class CustomModuleNotFoundError(ModuleNotFoundError, metaclass=ErrorMessageFormatter):
    pass


class CustomIndexError(IndexError, metaclass=ErrorMessageFormatter):
    pass


class TooManySpaces(CustomSyntaxError):
    ERROR_MESSAGE = "Too many spaces"


class TooManyBrackets(CustomSyntaxError):
    ERROR_MESSAGE = "Brackets are not balanced"


class TooManyArguments(CustomSyntaxError):
    ERROR_MESSAGE = "Too many arguments"


class UnrecognizedOperator(CustomValueError):
    ERROR_MESSAGE = "Unrecognized operator"


class UnrecognizedLexem(CustomValueError):
    ERROR_MESSAGE = "Unrecognized lexem"


class UnrecognizedFunc(CustomValueError):
    ERROR_MESSAGE = "Unrecognized Func"


class ModuleNotFound(CustomModuleNotFoundError):
    ERROR_MESSAGE = "Module aren't found"


class NotEnoughArguments(CustomIndexError):
    ERROR_MESSAGE = "Not enough arguments for operator"


class EmptyExpression(CustomIndexError):
    ERROR_MESSAGE = "Empty expressions aren't calculated"