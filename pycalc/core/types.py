class SingleTonClass(type):
    CLASSES = {}

    def __call__(cls, *args, **kwargs):
        if cls.__name__ in cls.CLASSES:
            return cls.CLASSES[cls.__name__]
        inst = super(SingleTonClass, cls).__call__(*args, **kwargs)
        cls.CLASSES[cls.__name__] = inst
        return inst


class Digit(metaclass=SingleTonClass):
    pass


class Operator(metaclass=SingleTonClass):
    pass


class MathExpr(metaclass=SingleTonClass):
    pass


class Bracket(metaclass=SingleTonClass):
    pass


class OpenBracket(Bracket):
    pass


class CloseBracket(Bracket):
    pass
