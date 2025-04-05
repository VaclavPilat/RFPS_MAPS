## \file
# Custom decorator functions for data classes.
# Method injection is preferred over subclassing
from types import FunctionType
from typing import Callable


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
    old_init = cls.__init__

    def new_init(self, *args, **kwargs) -> None:
        if getattr(self, "_argstring", None) is None:
            self._argstring = ", ".join(
                [repr(a) for a in args] + [f"{key}={repr(value)}" for (key, value) in kwargs.items()])
        old_init(self, *args, **kwargs)

    def new_repr(self) -> str:
        return f"{self.__class__.__name__}({self._argstring})"

    cls.__init__ = new_init
    cls.__repr__ = new_repr
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
    old_init = cls.__init__
    old_setattr = cls.__setattr__

    def new_init(self, *args, **kwargs) -> None:
        old_init(self, *args, **kwargs)
        self._initialised = True

    def new_setattr(self, name, value) -> None:
        if getattr(self, "_initialised", False):
            raise AttributeError(f"Attempting to modify {self.__class__.__name__}.{name}")
        # noinspection PyArgumentList
        old_setattr(self, name, value)

    cls.__init__ = new_init
    cls.__setattr__ = new_setattr
    return cls


# noinspection PyCallingNonCallable
def addCopyCall(*fields) -> Callable[[type], type]:
    """Creating a decorator the adds an automatic __call__ implementation.
    This function takes field names in the same order as constructor arguments.
    The new __call__ implementation creates a new instance from updated field values.

    Returns:
        func: Created class decorator function
    
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
        def new_call(self, *args, **kwargs) -> object:
            data = {field: getattr(self, field) for field in fields}
            for i in range(len(args)):
                data[fields[i]] = args[i]
            data.update(**kwargs)
            return cls(**data)

        cls.__call__ = new_call
        return cls

    return decorator


# noinspection PyTypeChecker
def defaultKwargsValues(*fields) -> Callable[[FunctionType], FunctionType]:
    """Creating a decorator that adds default values for kwargs from self fields.
    Providing new values in meant to be done only using kwargs.

    Returns:
        func: Decorator that adds default values to kwargs
    
    Examples:
        >>> class Test:
        ...     def __init__(self, value):
        ...             self.value = value
        ...     @defaultKwargsValues("value")
        ...     def stringify(self, value):
        ...             return str(value)
        ... 
        >>> Test(10).stringify()
        '10'
        >>> Test(10).stringify(value=20)
        '20'
    """

    def decorator(method: FunctionType):
        def wrapper(self, *args, **kwargs):
            data = {field: getattr(self, field) for field in fields}
            data.update(**kwargs)
            return method(self, *args, **data)

        return wrapper

    return decorator