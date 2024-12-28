## \file
# Testing autoRepr functionality
from Utils.Wrapper import autoRepr
import unittest



@autoRepr
class Wrapped:
    """Example class being wrapped
    """

    def __init__(self, value: int = 10):
        """Initialising an optional value

        Args:
            value (int, optional): Example value. Defaults to 10.
        """
        self.value = value



class AutoReprTest(unittest.TestCase):
    """Class for testing autoRepr implementation
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