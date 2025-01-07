## \file
# Testing autoRepr functionality
from Utils.Decorators import autoRepr
import unittest



@autoRepr
class Wrapped:
    """Example class being wrapped
    """

    def __init__(self, number: int = 10, string: str = ""):
        """Initialising an optional value

        Args:
            number (int, optional): Example number value. Defaults to 10.
            string (str, optional): Example string value. Defaults to "".
        """
        self.number = number
        self.string = string



class WrappedSubclass(Wrapped):
    """Subclass of the example wrapped class
    """
    pass



class AutoReprTest(unittest.TestCase):
    """Class for testing autoRepr implementation
    """

    def test_repr(self) -> None:
        """Testing repr() output
        """
        self.assertEqual(repr(Wrapped()), "Wrapped()")
        self.assertEqual(repr(Wrapped(5)), "Wrapped(5)")
        self.assertEqual(repr(Wrapped(0, "bar")), "Wrapped(0, 'bar')")
        self.assertEqual(repr(Wrapped(number=10)), "Wrapped(number=10)")
        self.assertEqual(repr(Wrapped(20, string="baz")), "Wrapped(20, string='baz')")
        self.assertEqual(repr(Wrapped(string="foo", number=0)), "Wrapped(string='foo', number=0)")
    
    def test_subclass(self) -> None:
        """Testing that the decorator still works on a subclass
        """
        self.assertEqual(repr(WrappedSubclass()), "WrappedSubclass()")
        self.assertEqual(repr(WrappedSubclass(5)), "WrappedSubclass(5)")
        self.assertEqual(repr(WrappedSubclass(0, "bar")), "WrappedSubclass(0, 'bar')")
        self.assertEqual(repr(WrappedSubclass(number=10)), "WrappedSubclass(number=10)")
        self.assertEqual(repr(WrappedSubclass(20, string="baz")), "WrappedSubclass(20, string='baz')")
        self.assertEqual(repr(WrappedSubclass(string="foo", number=0)), "WrappedSubclass(string='foo', number=0)")