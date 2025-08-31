"""! \file
Custom decorator functions for data classes.

These decorators either add additional functionality to existing classes or alter their behaviour.
Method injection is preferred over subclassing.

\todo Find a way to remove mentions of these decorators being called from exception tracebacks.
"""


def addInitRepr(cls: type) -> type:
    """Class decorator that adds __repr__ method.
    repr(obj) should return a string representation of the constructor call.

    Args:
        cls (type): Class type to wrap

    Returns:
        type: The same class type with updated members
    
    Examples:
        >>> @addInitRepr
        ... class Number:
        ...     def __init__(self, value=0):
        ...             self.value = value
        ... 
        >>> repr(Number())
        'Number()'
        >>> repr(Number(20))
        'Number(20)'
        >>> repr(Number(value=10))
        'Number(value=10)'
    """
    oldInit = cls.__init__

    def newInit(self, *args, **kwargs) -> None:
        if getattr(self, "_argstring", None) is None:
            self._argstring = ", ".join(
                [repr(a) for a in args] + [f"{key}={repr(value)}" for (key, value) in kwargs.items()])
        oldInit(self, *args, **kwargs)

    def newRepr(self) -> str:
        return f"{self.__class__.__name__}({self._argstring})"

    cls.__init__ = newInit
    cls.__repr__ = newRepr
    return cls


def makeImmutable(cls: type) -> type:
    """Class decorator that turns the class into an immutable one.
    Fields cannot be assigned after constructor is finished.

    Args:
        cls (type): Data class type to wrap

    Returns:
        type: The same class type with updated members
    
    Examples:
        >>> @makeImmutable
        ... class Number:
        ...     def __init__(self, value):
        ...             self.value = value
        ... 
        >>> Number(5).value
        5
        >>> Number(10).value = 20
        Traceback (most recent call last):
        AttributeError: Attempting to modify Number.value
    """
    oldInit = cls.__init__
    oldSetattr = cls.__setattr__

    def newInit(self, *args, **kwargs) -> None:
        oldInit(self, *args, **kwargs)
        self._initialised = True

    def newSetattr(self, name, value) -> None:
        if getattr(self, "_initialised", False):
            raise AttributeError(f"Attempting to modify {self.__class__.__name__}.{name}")
        # noinspection PyArgumentList
        oldSetattr(self, name, value)

    cls.__init__ = newInit
    cls.__setattr__ = newSetattr
    return cls


# noinspection PyCallingNonCallable
def addCopyCall(*fields):
    """Creating a decorator the adds an automatic __call__ implementation.
    This function takes field names in the same order as constructor arguments.
    The new __call__ implementation creates a new instance from updated field values.

    Returns:
        Class decorator
    
    Examples:
        >>> @addCopyCall("value")
        ... class Number:
        ...     def __init__(self, value=0):
        ...             self.value = value
        ... 
        >>> Number()(10).value
        10
        >>> Number(20)().value
        20
        >>> Number(30)(value=-5).value
        -5
    """

    def decorator(cls: type) -> type:
        def newCall(self, *args, **kwargs) -> object:
            data = {field: getattr(self, field) for field in fields}
            for i in range(len(args)):
                data[fields[i]] = args[i]
            data.update(**kwargs)
            return cls(**data)

        cls.__call__ = newCall
        return cls

    return decorator


# noinspection PyUnresolvedReferences
def mirrorOperators(cls: type) -> type:
    """A class decorator for adding counterparts of already defined math operators.
    Some predefined "mirror operations" will be added.

    Args:
        cls (type): Data class type to add operators to

    Returns:
        type: The same class type with added operators

    Examples:
        >>> @mirrorOperators
        ... class Number:
        ...     def __init__(self, value):
        ...         self.value = value
        ...     def __neg__(self):
        ...         return Number(-self.value)
        ...     def __add__(self, other):
        ...         return Number(self.value + other.value)
        ...
        >>> (Number(3) - Number(7)).value
        -4
    """

    def createOperator(operation: str):
        def operator(self, other):
            return getattr(self, operation)(-other)

        return operator

    for positive, negative in {"__add__": "__sub__", "__rshift__": "__lshift__"}.items():
        if hasattr(cls, positive) and not hasattr(cls, negative):
            setattr(cls, negative, createOperator(positive))
    return cls