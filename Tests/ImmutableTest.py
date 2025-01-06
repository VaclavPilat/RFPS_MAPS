## \file
# Testing immutable decorator functionality
from Utils.Wrapper import immutable
import unittest



@immutable
class Wrapped:
    """Example class being wrapped
    """

    def __init__(self, value: int = 10):
        """Initialising an optional value

        Args:
            value (int, optional): Example value. Defaults to 10.
        """
        self.value = value



class WrappedSubclass(Wrapped):
    """Subclass of the example wrapped class
    """
    pass



class ImmutableTest(unittest.TestCase):
    """Class for testing immutable implementation
    """

    def test_value(self) -> None:
        """Testing field value
        """
        self.assertEqual(Wrapped().value, 10)
        self.assertEqual(Wrapped(5).value, 5)

    def test_assignment(self) -> None:
        """Testing field value (re)assignment
        """
        x = Wrapped()
        with self.assertRaises(AttributeError):
            x.value = 15
        with self.assertRaises(AttributeError):
            x.foo = "bar"
    
    def test_subclass(self) -> None:
        """Testing that the decorator still works even when subclassing
        """
        self.assertEqual(WrappedSubclass(value=20).value, 20)
        with self.assertRaises(AttributeError):
            WrappedSubclass().value = 10