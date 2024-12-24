## \file
# Wrapper functions



def reprWrapper(cls: "cls") -> "cls":
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



if __name__ == "__main__":
    @reprWrapper
    class Wrapped:
        """Example class being wrapped
        """
        def __init__(self, value: int = 10):
            """Initialising an optional value

            Args:
                value (int, optional): Example value. Defaults to 10.
            """
            self.value = value
    import unittest
    class ReprWrapperTest(unittest.TestCase):
        """Class for testing @reprWrapper implementation
        """
        def test_repr(self) -> None:
            """Testing repr() output
            """
            self.assertEqual(repr(Wrapped()), "Wrapped()")
            self.assertEqual(repr(Wrapped(5)), "Wrapped(5)")
        def test_fields(self) -> None:
            """Testing field value
            """
            self.assertEqual(Wrapped().value, 10)
            self.assertEqual(Wrapped(5).value, 5)
    unittest.main()