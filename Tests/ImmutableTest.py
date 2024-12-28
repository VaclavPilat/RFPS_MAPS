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



class ImmutableTest(unittest.TestCase):
    """Class for testing immutable implementation
    """

    def test_value(self) -> None:
        """Testing field value
        """
        self.assertEqual(Wrapped().value, 10)
        self.assertEqual(Wrapped(5).value, 5)

    def test_reassignment(self) -> None:
        """Testing field value reassignment
        """
        x = Wrapped()
        with self.assertRaises(AttributeError):
            x.value = 15

    def test_assignment(self) -> None:
        """Testing field value reassignment
        """
        x = Wrapped(5)
        with self.assertRaises(AttributeError):
            x.foo = "bar"