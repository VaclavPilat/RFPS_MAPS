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
        return IUnion(self, other)

    def __str__(self) -> str:
        """Getting string representation of this interval operator

        Raises:
            NotImplemented: Thrown when not overwritten

        Returns:
            str: String representation of this interval operator
        """
        raise NotImplemented
    
    def generate(self, *args, **kwargs) -> list:
        """Generating values from within the interval

        Raises:
            NotImplemented: Thrown when not overwritten

        Returns:
            tuple: List of generated values
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
    
    def generate(self, *args, **kwargs) -> list:
        """Generating values from an interval intersection

        Returns:
            tuple: List of generated values
        """
        values = self.intervals[0].generate(*args, **kwargs)
        for i in self.intervals[1:]:
            values = (x for x in values if x in i.generate(*args, **kwargs))
        return values



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
    
    def generate(self, *args, **kwargs) -> list:
        """Generating values from an interval union

        Returns:
            tuple: List of generated values
        """
        values = []
        for i in self.intervals:
            for x in i.generate(*args, **kwargs):
                if x not in values:
                    values.append(x)
        return values



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
        assert lower <= upper, "Lower bound has to be lesser than or equal to the upper one"
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
            upper (int | float): Unclamped upper bound

        Returns:
            IOperator: Interval operator
        """
        lower, upper = (x if 0 <= x <= 360 else x % 360 for x in (lower, upper))
        if lower < upper:
            return I360(lower, upper)
        return I360(lower, 360) | I360(0, upper)
    
    def generate(self, points: int) -> list:
        """Generating points on a circle

        Args:
            points (int): Number of points to generate

        Returns:
            tuple: Generated points
        """
        return [p % 360 for p in (360 * i / points for i in range(points + 1)) if p in self]