from typing import Type, Dict, Any


class SingleTonClass(type):
    CLASSES: Dict[str, Type[Any]] = {}

    def __call__(cls, *args, **kwargs):
        if cls.__name__ in cls.CLASSES:
            return cls.CLASSES[cls.__name__]
        inst = super(SingleTonClass, cls).__call__(*args, **kwargs)
        cls.CLASSES[cls.__name__] = inst
        return inst


class CustomType(metaclass=SingleTonClass):
    pass


class Digit(CustomType):
    pass


class Operator(CustomType):
    pass


class MathExpr(CustomType):
    pass


class Bracket(CustomType):
    pass


class OpenBracket(Bracket):
    pass


class CloseBracket(Bracket):
    pass
