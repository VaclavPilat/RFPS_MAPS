## \file
# Testing implementation of a defaultKwargsValues decorator
from Utils.Decorators import defaultKwargsValues
import unittest



class Single:
    """Example class with wrapped single argument methods
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



class Multiple:
    """Example class with wrapped multiple argument methods
    """

    def __init__(self, a: int = 0, b: int = 0, c: int = 0) -> None:
        """Initialising a value

        Args:
            a (int, optional): A value. Defaults to 0.
            b (int, optional): B value. Defaults to 0.
            c (int, optional): C value. Defaults to 0.
        """
        self.a = a
        self.b = b
        self.c = c
    
    @defaultKwargsValues("a", "b", "c")
    def sum(self, a: int, b: int, c: int) -> int:
        """Getting the sum of all three values
        """
        return a + b + c



class DefaultKwargsValuesTest(unittest.TestCase):
    """Class for testing defaultKwargsValues functionality
    """

    def test_single(self) -> None:
        """Testing single value method calls
        """
        for method in (Single.arg, Single.kwarg, Single.kwargdict):
            self.assertEqual(method(Single()), 0)
            self.assertEqual(method(Single(10)), 10)
            self.assertEqual(method(Single(), value=5), 5)
            self.assertEqual(method(Single(20), value=10), 10)

    def test_multiple(self) -> None:
        """Testing multiple values 
        """
        self.assertEqual(Multiple().sum(), 0)
        self.assertEqual(Multiple(1, 1, 1).sum(), 3)
        self.assertEqual(Multiple(1, 2, 3).sum(), 6)
        self.assertEqual(Multiple(1).sum(), 1)
        self.assertEqual(Multiple(1).sum(a=2), 2)
        self.assertEqual(Multiple().sum(b=10, c=5), 15)