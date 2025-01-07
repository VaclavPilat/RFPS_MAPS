## \file
# Custom decorator/wrapper functions for data classes.
# Method injection is preferred over subclassing



def autoRepr(cls: "cls") -> "cls":
    """Class wrapper that adds __repr__ method.
    repr(obj) should return a string representation of the constructor call.

    Args:
        cls (cls): Class type to wrap

    Returns:
        cls: The same class type with updated members
    
    Examples:
        >>> @autoRepr
        ... class Wrapped:
        ...     pass
        ... 
    """
    old_init = cls.__init__
    def new_init(self, *args, **kwargs) -> None:
        self._argstring = ", ".join([repr(a) for a in args] + [f"{key}={repr(value)}" for (key, value) in kwargs.items()])
        old_init(self, *args, **kwargs)
    def new_repr(self) -> str:
        return f"{self.__class__.__name__}({self._argstring})"
    cls.__init__ = new_init
    cls.__repr__ = new_repr
    return cls



## \todo Add recursive behaviour - restricting value changes on inner fields
def immutable(cls: "cls") -> "cls":
    """Class wrapper that turns the class into an immutable one

    Args:
        cls (cls): Data class type to wrap

    Returns:
        cls: The same class type with updated members
    
    Examples:
        >>> @immutable
        ... class Wrapped:
        ...     pass
        ... 
    """
    old_init = cls.__init__
    old_setattr = cls.__setattr__
    def new_init(self, *args, **kwargs) -> None:
        old_init(self, *args, **kwargs)
        self._initialised = True
    def new_setattr(self, name, value) -> None:
        if getattr(self, "_initialised", False):
            raise AttributeError(f"Attempting to modify {self.__class__.__name__}.{name}")
        old_setattr(self, name, value)
    cls.__init__ = new_init
    cls.__setattr__ = new_setattr
    return cls



def autoCall(*fields) -> "func":
    """Creating a decorator the adds an automatic __call__ implementation.
    This function takes field names in the same order as constructor arguments.
    The new __call__ implementation creates a new instance from updated field values.

    Returns:
        func: Created class decorator function
    """
    def decorator(cls: "cls") -> "cls":
        def new_call(self, *args, **kwargs) -> "obj":
            data = {field: getattr(self, field) for field in fields}
            for i in range(len(args)):
                data[fields[i]] = args[i]
            data.update(**kwargs)
            return cls(**data)
        cls.__call__ = new_call
        return cls
    return decorator