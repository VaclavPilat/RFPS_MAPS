## \file
# Interval classes
from Utils.Decorators import addInitRepr, makeImmutable, addCopyCall



@makeImmutable
class IOperator:
    """Class for containing common interval operations
    """

    def __contains__(self, number: int|float) -> bool:
        """Checking whether a number is within an interval

        Args:
            number (int | float): Number value to check

        Raises:
            NotImplemented: Thrown when not overwritten

        Returns:
            bool: True if number belongs to the interval
        """
        raise NotImplemented
    
    def __and__(self, other: "IOperator") -> "IIntersect":
        """Creating an intersection of intervals

        Args:
            other (IOperator): Other interval

        Returns:
            Interval: Intersection of this and the other interval
        """
        return IIntersect(self, other)

    def __or__(self, other: "IOperator") -> "IUnion":
        """Creating a union of intervals

        Args:
            other (IOperator): Other interval

        Returns:
            Interval: Union of this and the other interval
        """
        pass

    def __str__(self) -> str:
        """Getting string representation of this interval operator

        Raises:
            NotImplemented: Thrown when not overwritten

        Returns:
            str: String representation of this interval operator
        """
        raise NotImplemented



class IIntersect(IOperator):
    """Class for containing multiple intervals in an intersection
    """

    def __init__(self, *intervals) -> None:
        """Initialising an interval intersection
        """
        self.intervals = intervals
    
    def __contains__(self, number: int|float) -> bool:
        """Checking whether a number is within this interval intersection

        Args:
            number (int | float): Number value to check

        Returns:
            bool: True if the number is within all intervals
        """
        for interval in self.intervals:
            if number not in interval:
                return False
        return True
    
    def __str__(self) -> str:
        """Getting string representation of an interval intersection

        Returns:
            str: String representation
        """
        return "(" + " & ".join(self.intervals) + ")"



class IUnion(IOperator):
    """Class for containing multiple intervals in a union
    """

    def __init__(self, *intervals) -> None:
        """Initialising an interval union
        """
        self.intervals = intervals
    
    def __contains__(self, number: int|float) -> bool:
        """Checking whether a number is within this interval union

        Args:
            number (int | float): Number value to check

        Returns:
            bool: True if the number is within at least one of the intervals
        """
        for interval in self.intervals:
            if number in interval:
                return True
        return False
    
    def __str__(self) -> str:
        """Getting string representation of an interval union

        Returns:
            str: String representation
        """
        return "(" + " | ".join(self.intervals) + ")"



@addInitRepr
@addCopyCall("lower", "upper")
class Interval(IOperator):
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
        try:
            assert lower < upper, "Lower bound has to be lesser than the upper one"
        except:
            print(lower, upper)
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
    
    @staticmethod
    def clamp(lower: int|float, upper: int|float) -> "IOperator":
        """Creating an interval from unclamped degree values

        Args:
            lower (int | float): Unclamped lower bound
            upper (int | float): Unclamped upepr bound

        Returns:
            IOperator: Interval operator
        """
        assert lower < upper, "Lower bound has to be lesser than upper bound"
        lower, upper = (x if 0 <= x <= 360 else x % 360 for x in (lower, upper))
        if lower < upper:
            return I360(lower, upper)
        ## \todo fix the 359 number by adding the ability to exclude bound(s)
        return IUnion(I360(0, upper), I360(lower, 359))