## \file
# Custom decorator functions for data classes.
# Method injection is preferred over subclassing


def addInitRepr(cls: type) -> type:
    """Class decorator that adds __repr__ method.
    repr(obj) should return a string representation of the constructor call.

    Args:
        cls (type): Class type to wrap

    Returns:
        type: The same class type with updated members
    
    Examples:
        >>> @addInitRepr
        ... class Wrapped:
        ...     def __init__(self, value=0):
        ...             self.value = value
        ... 
        >>> repr(Wrapped())
        'Wrapped()'
        >>> repr(Wrapped(20))
        'Wrapped(20)'
        >>> repr(Wrapped(value=10))
        'Wrapped(value=10)' 
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
    """Class decorator that turns the class into an immutable one

    Args:
        cls (type): Data class type to wrap

    Returns:
        type: The same class type with updated members
    
    Examples:
        >>> @makeImmutable
        ... class Wrapped:
        ...     def __init__(self, value):
        ...             self.value = value
        ... 
        >>> Wrapped(5).value
        5
        >>> Wrapped(10).value = 20
            ...
        AttributeError: Attempting to modify Wrapped.value 
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
        ... class Wrapped:
        ...     def __init__(self, value=0):
        ...             self.value = value
        ... 
        >>> Wrapped()(10).value
        10
        >>> Wrapped(20)().value
        20
        >>> Wrapped(30)(value=-5).value
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