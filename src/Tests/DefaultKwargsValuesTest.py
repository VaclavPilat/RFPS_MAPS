## \file
# Testing implementation of a defaultKwargsValues decorator
from Utils.Decorators import defaultKwargsValues
import unittest



class Wrapped:
    """Example class with wrapped methods
    """

    def __init__(self, value: int = 0) -> None:
        """Initialising a value

        Args:
            value (int, optional): Example value. Defaults to 0.
        """
        self.value = value
    
    @defaultKwargsValues("value")
    def arg(self, value: int) -> int:
        """Using a default value for an arg

        Args:
            value (int): Arg value

        Returns:
            int: Arg value or its default value
        """
        return value
    
    @defaultKwargsValues("value")
    def kwarg(self, value: int = None) -> int:
        """Using a default value for a kwarg

        Args:
            value (int, optional): Value will be replaced. Defaults to None.

        Returns:
            int: Kwarg value or its default value
        """
        return value
    
    @defaultKwargsValues("value")
    def kwargdict(self, **kwargs) -> int:
        """Using a default value in a kwarg dict

        Returns:
            int: Kwarg value or its default value
        """
        return kwargs["value"]



class DefaultKwargsValuesTest(unittest.TestCase):
    """Class for testing defaultKwargsValues functionality
    """

    def test_calls(self) -> None:
        """Testing single value method calls
        """
        for method in (Wrapped.arg, Wrapped.kwarg, Wrapped.kwargdict):
            self.assertEqual(method(Wrapped()), 0)
            self.assertEqual(method(Wrapped(10)), 10)
            self.assertEqual(method(Wrapped(), value=5), 5)
            self.assertEqual(method(Wrapped(20), value=10), 10)