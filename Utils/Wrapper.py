## \file
# Custom decorator/wrapper functions for data classes.
# Method injection is preferred over subclassing



def initRepr(cls: "cls") -> "cls":
    """Class wrapper that adds __repr__ method.
    repr(obj) should return a string representation of the constructor call.

    Args:
        cls (cls): Class type to wrap

    Returns:
        cls: The same class type with updated members
    """
    old_init = cls.__init__
    def new_init(self, *args, **kwargs) -> None:
        self.argstring = ", ".join([repr(a) for a in args] + [f"{key}={repr(value)}" for (key, value) in kwargs.items()])
        old_init(self, *args, **kwargs)
    def new_repr(self) -> str:
        return f"{self.__class__.__name__}({self.argstring})"
    cls.__init__ = new_init
    cls.__repr__ = new_repr
    return cls