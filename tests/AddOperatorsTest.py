## \file
# Tests for addOperators functionality
from src.Utils.Decorators import addOperators
import unittest


# noinspection IncorrectFormatting
@addOperators
class Wrapped:
    """Example class being wrapped
    """

    def __init__(self, value: int) -> None:
        """Initialising an instance

        Args:
            value (int): Number value
        """
        self.value = value

    def __neg__(self) -> "Wrapped":
        """Negating a number

        Returns:
            Wrapped: Instance with a negated value
        """
        return Wrapped(-self.value)

    def __add__(self, other: "Wrapped") -> "Wrapped":
        """Adding two numbers

        Args:
            other (Number): Number to be added

        Returns:
            Number: Sum of two numbers
        """
        return Wrapped(self.value + other.value)

    def __rshift__(self, other: int) -> "Wrapped":
        """Moving the decimal place right by a number of digits

        Args:
            other (int): Number of digits to move the decimal place by

        Returns:
            Wrapped: Number shifted by an amount of digits
        """
        return Wrapped(self.value * pow(10, -other))


class AddOperatorsTest(unittest.TestCase):
    """Testing the functionality of the addOperators decorator
    """

    def test_subtraction(self) -> None:
        """Testing the subtraction operator
        """
        self.assertEqual((Wrapped(1) + Wrapped(3)).value, 4)
        self.assertEqual((Wrapped(1) - Wrapped(3)).value, -2)

    def test_lshift(self) -> None:
        """Testing the lshift operator
        """
        self.assertEqual((Wrapped(2) >> 3).value, 0.002)
        self.assertEqual((Wrapped(2) << 3).value, 2000)