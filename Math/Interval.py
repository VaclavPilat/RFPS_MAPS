## \file
# Interval classes
from Utils.Decorators import addInitRepr, makeImmutable, addCopyCall



@addInitRepr
@makeImmutable
@addCopyCall("lower", "upper")
class Interval:
    """Class for an interval
    """

    def __init__(self, lower: int|float, upper: int|float) -> None:
        """Initializing the interval

        Args:
            lower (int | float): Interval lower bound
            upper (int | float): Interval upper bound
        
        Examples:
            >>> Interval(0, 100)
            Interval(0, 100)
            >>> Interval(90, 270)
            Interval(90, 270)
        """
        assert lower < upper, "Lower bound has to be lesser than the upper one"
        ## Interval lower bound
        self.lower = lower
        ## Interval upper bound
        self.upper = upper
    
    def __contains__(self, number: int|float) -> bool:
        """Checking whether a number is within this interval

        Args:
            number (int | float): Number value to check

        Returns:
            bool: True if the number is within the interval bounds
        
        Examples:
            >>> 50 in Interval(0, 100)
            True
            >>> 180 in Interval(0, 90)
            False
        """
        return self.lower <= number <= self.upper



class I360(Interval):
    """Interval of degrees on a circle
    """

    def __init__(self, lower: int|float, upper: int|float) -> None:
        """Initialising the interval

        Args:
            lower (int | float): Lower bound value
            upper (int | float): Upper bound value
        """
        for angle in (lower, upper):
            assert 0 <= angle <= 360, "Both angle bounds have to be between 0 and 360"
        super().__init__(lower, upper)