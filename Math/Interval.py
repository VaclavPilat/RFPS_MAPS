## \file
# Interval classes.
# The "I" in front of some class names stands for "Interval"
from Utils.Decorators import addInitRepr, makeImmutable, addCopyCall



@makeImmutable
class IOperator:
    """Class for containing common interval operations.
    Immutable.
    """

    def __contains__(self, number: int|float) -> bool:
        """Checking whether a number is within an interval

        Args:
            number (int | float): Number value to check

        Raises:
            NotImplementedError: Thrown when not overwritten

        Returns:
            bool: True if number belongs to the interval
        """
        raise NotImplementedError
    
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

    def __repr__(self) -> str:
        """Getting string representation of this interval operator

        Raises:
            NotImplementedError: Thrown when not overwritten

        Returns:
            str: String representation of this interval operator
        """
        raise NotImplementedError
    
    def generate(self, *args, **kwargs) -> list:
        """Generating values from within the interval

        Raises:
            NotImplementedError: Thrown when not overwritten

        Returns:
            tuple: List of generated values
        """
        raise NotImplementedError
    
    def __invert__(self) -> "IOperator":
        """Inverting the interval

        Raises:
            NotImplementedError: Thrown when not overwritten

        Returns:
            IOperator: Inverted operator
        """
        raise NotImplementedError
    
    def __add__(self, number: int|float) -> "IOperator":
        """Incrementing an interval by a number

        Args:
            number (int | float): Number value to add

        Raises:
            NotImplementedError: Thrown when not overwritten

        Returns:
            IOperator: Incremented interval
        """
        raise NotImplementedError



class IIntersect(IOperator):
    """Class for containing multiple intervals in an intersection
    """

    def __init__(self, *intervals) -> None:
        """Initialising an interval intersection
        """
        self.intervals = intervals
        super().__init__()
    
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
    
    def __repr__(self) -> str:
        """Getting string representation of an interval intersection

        Returns:
            str: String representation
        """
        return "(" + " & ".join((str(x) for x in self.intervals)) + ")"
    
    def generate(self, *args, **kwargs) -> list:
        """Generating values from an interval intersection

        Returns:
            tuple: List of generated values
        """
        values = self.intervals[0].generate(*args, **kwargs)
        for i in self.intervals[1:]:
            values = [x for x in values if x in i.generate(*args, **kwargs)]
        return values
    
    def __invert__(self) -> "IUnion":
        """Inverts an intersection of intervals

        Returns:
            IUnion: Union of inverted intervals
        """
        return IUnion(*[~i for i in self.intervals])
    
    def __add__(self, number: int|float) -> "IIntersect":
        """Incrementing an intersection of intervals

        Args:
            number (int | float): Number to increment by

        Returns:
            IIntersect: Incremented interval intersection
        """
        return IIntersect(*[x + number for x in self.intervals])



class IUnion(IOperator):
    """Class for containing multiple intervals in a union
    """

    def __init__(self, *intervals) -> None:
        """Initialising an interval union
        """
        self.intervals = intervals
        super().__init__()
    
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
    
    def __repr__(self) -> str:
        """Getting string representation of an interval union

        Returns:
            str: String representation
        """
        return "(" + " | ".join((str(x) for x in self.intervals)) + ")"
    
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
    
    def __invert__(self) -> "IIntersect":
        """Inverts a union of intervals

        Returns:
            IIntersect: Intersection of inverted intervals
        """
        return IIntersect(*[~i for i in self.intervals])
    
    def __add__(self, number: int|float) -> "IUnion":
        """Incrementing a union of intervals

        Args:
            number (int | float): Number to increment by

        Returns:
            IUnion: Incremented interval union
        """
        return IUnion(*[x + number for x in self.intervals])



@addInitRepr
class Interval(IOperator):
    """Class for an interval
    """

    def __init__(self, lower: int|float, upper: int|float, includeLower: bool = True, includeUpper: bool = True) -> None:
        """Initializing the interval

        Args:
            lower (int | float): Interval lower bound
            upper (int | float): Interval upper bound
            includeLower (bool, optional): Should lower bound be included? Defaults to True.
            includeUpper (bool, optional): Should upper bound be included? Defaults to True.
        
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
        ## Should the lower bound be included?
        self.includeLower = includeLower
        ## Should the upper bound be included?
        self.includeUpper = includeUpper
    
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
        if number == self.lower:
            return self.includeLower
        if number == self.upper:
            return self.includeUpper
        return self.lower <= number <= self.upper



class I360(Interval):
    """Interval of degrees on a circle
    """

    def __init__(self, lower: int|float = 0, upper: int|float = 360, *args, **kwargs) -> None:
        """Initialising the interval

        Args:
            lower (int | float, optional): Lower bound. Defaults to 0.
            upper (int | float, optional): Upper bound. Defaults to 360.
        """
        for angle in (lower, upper):
            assert 0 <= angle <= 360, "Both angle bounds have to be between 0 and 360"
        super().__init__(lower, upper, *args, **kwargs)
    
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
        """Generating angles that belong to the interval

        Args:
            points (int): Number of angles to generate

        Returns:
            tuple: Generated angle values
        """
        return [p % 360 for p in (360 * i / points for i in range(points + 1)) if p in self]
    
    def __invert__(self) -> "IOperator":
        """Inverting an interval

        Returns:
            IOperator: Inverted interval or a union of intervals
        """
        if 0 < self.lower <= self.upper < 360:
            return I360(self.upper, 360, includeLower=not self.includeUpper, includeUpper=False) | I360(0, self.lower, includeLower=True, includeUpper=not self.includeLower)
        if self.lower == 0:
            return I360(self.upper, 360, includeLower=not self.includeUpper, includeUpper=not self.includeLower)
        return I360(0, self.lower, includeLower=not self.includeUpper, includeUpper=not self.includeLower)
    
    def __add__(self, number: int|float) -> "IOperator":
        """Incrementing a circular interval

        Args:
            number (int | float): Number to increment by

        Returns:
            IOperator: Either a I360 instance or a union of them
        """
        return self.clamp(self.lower + number, self.upper + number)