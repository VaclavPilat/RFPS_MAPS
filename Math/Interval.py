## \file
# Implementation of interval classes
from Utils.Decorators import addCopyCall, makeImmutable, addInitRepr



@makeImmutable
class IOperand:
    """Abstract class for containing common interval operation definitions.

    Made immutable by using a decorator.
    """
    
    def __and__(self, other: "IOperand") -> "IIntersect":
        """Creating an intersection of intervals

        Args:
            other (IOperand): Other interval

        Returns:
            IIntersect: Intersection of this and the other interval
        """
        return IIntersect(self, other)

    def __or__(self, other: "IOperand") -> "IUnion":
        """Creating a union of intervals

        Args:
            other (IOperand): Other interval

        Returns:
            IUnion: Union of this and the other interval
        """
        return IUnion(self, other)


class IIntersect(IOperand):
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
    
    def __invert__(self) -> "IUnion":
        """Inverts an intersection of intervals

        Returns:
            IUnion: Union of inverted intervals
        """
        return IUnion(*[~i for i in self.intervals])
    
    def __repr__(self) -> str:
        """Getting string representation of an interval intersection

        Returns:
            str: String representation
        """
        return "(" + " & ".join((str(x) for x in self.intervals)) + ")"
    
    def generate(self, *args, **kwargs) -> list:
        """Generating values from an interval intersection

        Returns:
            list: List of generated values
        """
        values = self.intervals[0].generate(*args, **kwargs)
        for i in self.intervals[1:]:
            values = [x for x in values if x in i.generate(*args, **kwargs)]
        return values
    
    def __add__(self, number: int|float) -> "IIntersect":
        """Incrementing an intersection of intervals

        Args:
            number (int | float): Number to increment by

        Returns:
            IIntersect: Incremented interval intersection
        """
        return IIntersect(*[x + number for x in self.intervals])



class IUnion(IOperand):
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
    
    def __invert__(self) -> "IIntersect":
        """Inverts a union of intervals

        Returns:
            IIntersect: Intersection of inverted intervals
        """
        return IIntersect(*[~i for i in self.intervals])
    
    def __repr__(self) -> str:
        """Getting string representation of an interval union

        Returns:
            str: String representation
        """
        return "(" + " | ".join((str(x) for x in self.intervals)) + ")"
    
    def generate(self, *args, **kwargs) -> list:
        """Generating values from an interval union

        Returns:
            list: List of generated values
        """
        values = []
        for i in self.intervals:
            for x in i.generate(*args, **kwargs):
                if x not in values:
                    values.append(x)
        return values
    
    def __add__(self, number: int|float) -> "IUnion":
        """Incrementing a union of intervals

        Args:
            number (int | float): Number to increment by

        Returns:
            IUnion: Incremented interval union
        """
        return IUnion(*[x + number for x in self.intervals])



@addInitRepr
@addCopyCall("start", "end", "openStart", "openEnd")
class I360(IOperand):
    """Class for representing a circular interval from 0 to 360 degrees

    This class is made immutable and has automatic __repr__ and __call__ using decorators.
    """

    def __init__(self, start: int|float = 0, end: int|float = 360, openStart: bool = False, openEnd: bool = False) -> None:
        """Initialising a circular interval

        Args:
            start (int | float, optional): Start value. Defaults to 0.
            end (int | float, opetional): End value. Defaults to 360.
            openStart (bool, optional): Should the start of the interval be open? Defaults to False.
            openEnd (bool, optional): Should the end of the interval be open? Defaults to False.
        """
        assert 0 <= start <= end <= 360, "Both bounds have to be between 0 and 360, start cannot be greater than end"
        ## Interval start bound value
        self.start = start
        ## Interval end bound value
        self.end = end
        ## Is interval open at start?
        self.openStart = openStart
        ## Is interval open at end?
        self.openEnd = openEnd
        ## Is the interval empty?
        self.isEmpty = start == end and openStart and openEnd
        ## Is the interval the whole circle?
        self.isFull = start == 0 and end == 360 and (not openStart or not openEnd)
        super().__init__()
    
    def __contains__(self, number: int|float) -> bool:
        """Checking whether a number belongs to the interval

        Args:
            number (int | float): Number value to check

        Returns:
            bool: True if the number within interval bounds
        """
        if self.isEmpty:
            return False
        startCondition = (self.start < number) if self.openStart else (self.start <= number)
        endCondition = (number < self.end) if self.openEnd else (number <= self.end)
        return startCondition and endCondition
    
    def __invert__(self) -> "IOperand":
        """Inverting current interval

        Returns:
            IOperand: An interval that covers the rest of the circle
        """
        if self.isEmpty:
            return I360(0, 360, False, False)
        if self.isFull:
            return I360(0, 0, True, True)
        if self.start == 0:
            return I360(self.end, 360, not self.openEnd, not self.openStart)
        if self.end == 360:
            return I360(0, self.start, not self.openEnd, not self.openStart)
        return I360(self.end, 360, not self.openEnd) | I360(0, self.start, False, not self.openStart)
    
    def generate(self, points: int) -> list:
        """Generating angles that belong to the interval

        Args:
            points (int): Number of angles to generate

        Returns:
            list: Generated angle values
        """
        return [p % 360 for p in (360 * i / points for i in range(points + 1)) if p in self]
    
    @staticmethod
    def clamp(start: int|float, end: int|float, openStart: bool = False, openEnd: bool = False) -> "IOperand":
        """Creating an interval from unclamped degree values

        Args:
            start (int | float): Unclamped start value
            end (int | float): Unclamped end value
            openStart (bool, optional): Should the start of the interval be open? Defaults to False.
            openEnd (bool, optional): Should the end of the interval be open? Defaults to False.

        Returns:
            IOperand: Interval operator
        """
        start, end = (x if 0 <= x <= 360 else x % 360 for x in (start, end))
        if start < end:
            return I360(start, end, openStart, openEnd)
        return I360(start, 360, openStart, True) | I360(0, end, False, openEnd)
    
    def __add__(self, number: int|float) -> "IOperand":
        """Incrementing a circular interval

        Args:
            number (int | float): Number to increment by

        Returns:
            IOperand: Either a I360 instance or a union of them
        """
        return self.clamp(self.start + number, self.end + number, self.openStart, self.openEnd)



## An enpty interval, equals to I360(0, 0, False, False)
I360.EMPTY = I360(0, 0)
## A full interval, equals to I360(0, 360, True, True)
I360.FULL = I360(0, 360, True, True)