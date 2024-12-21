## \file
# Wrapper functions



def reprWrapper(cls: "cls") -> "cls":
    """Class wrapper that returns a subclass of the wrapped one
    Adds a __repr__ method that returns a representation of the construction call

    Args:
        cls (cls): Class type to wrap

    Returns:
        cls: Subclass type of the wrapped class
    """
    class reprWrapped(cls):
        """Wrapped class
        """
        def __init__(self, *args, **kwargs) -> None:
            """Initializing the argstring an calling wrapped class constructor
            """
            self.argstring = ", ".join([repr(a) for a in args] + [f"{key}={repr(value)}" for (key, value) in kwargs.items()])
            super().__init__(*args, **kwargs)
        def __repr__(self) -> str:
            """Returns string representation of a constructor call

            Returns:
                str: String representing constructor call
            """
            name = cls.__name__ if self.__class__ == reprWrapped else self.__class__.__name__
            return f"{name}({self.argstring})"
    return reprWrapped