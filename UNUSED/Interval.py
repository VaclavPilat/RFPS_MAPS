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
        
        Examples:
            >>> I360(0, 180) & I360(75, 135)
            (I360(0, 180) & I360(75, 135))
            >>> I360(90, 120) & I360(150, 180)
            (I360(90, 120) & I360(150, 180))
        """
        return IIntersect(self, other)

    def __or__(self, other: "IOperand") -> "IUnion":
        """Creating a union of intervals

        Args:
            other (IOperand): Other interval

        Returns:
            IUnion: Union of this and the other interval
        
        Examples:
            >>> I360(0, 90) | I360(60, 120)
            (I360(0, 90) | I360(60, 120))
            >>> I360(0, 120) | I360(180, 270)
            (I360(0, 120) | I360(180, 270))
        """
        return IUnion(self, other)
    
    def __sub__(self, number: int|float) -> "IOperand":
        """Subtracting a number from an interval

        Args:
            number (int | float): Number to subtract by

        Returns:
            IOperand: Subtracted interval operand
        """
        return self.__add__(-number)



class IIntersect(IOperand):
    """Class for containing multiple intervals in an intersection
    """

    def __init__(self, *intervals) -> None:
        """Initialising an interval intersection

        Examples:
            >>> IIntersect(I360(0, 90), I360(60, 120), I360(90, 120))
            (I360(0, 90) & I360(60, 120) & I360(90, 120))
        """
        ## Intervals that are a part of the intersection
        self.intervals = intervals
        super().__init__()
    
    def __contains__(self, number: int|float) -> bool:
        """Checking whether a number is within this interval intersection

        Args:
            number (int | float): Number value to check

        Returns:
            bool: True if the number is within all intervals
        
        Examples:
            >>> 60 in I360(0, 180) & I360(75, 135)
            False
            >>> 120 in I360(0, 180) & I360(75, 135)
            True
        """
        for interval in self.intervals:
            if number not in interval:
                return False
        return True
    
    def __invert__(self) -> "IUnion":
        """Inverts an intersection of intervals

        Returns:
            IUnion: Union of inverted intervals
        
        Examples:
            >>> ~(I360(60, 120) & I360(90, 180))
            ((I360(120, 360, True) | I360(0, 60, False, True)) | (I360(180, 360, True) | I360(0, 90, False, True)))
        """
        return IUnion(*[~i for i in self.intervals])
    
    def __repr__(self) -> str:
        """Getting string representation of an interval intersection

        Returns:
            str: String representation
        
        Examples:
            >>> repr(I360(0, 120) | I360(180, 270))
            '(I360(0, 120) | I360(180, 270))'
        """
        return "(" + " & ".join((str(x) for x in self.intervals)) + ")"
    
    def __iter__(self) -> list:
        """Generating values from an interval intersection
        
        Examples:
            >>> list((I360(0, 180, points=16) & I360(75, 135, points=16)))
            [90.0, 112.5, 135.0]
            >>> list((I360(0, 90, points=36) & I360(120, 180, points=36)))
            []
        """
        values = list(self.intervals[0])
        for interval in self.intervals[1:]:
            values = [x for x in values if x in list(interval)]
        return iter(values)
    
    def __add__(self, number: int|float) -> "IIntersect":
        """Incrementing an intersection of intervals

        Args:
            number (int | float): Number to increment by

        Returns:
            IIntersect: Incremented interval intersection
        
        Examples:
            >>> (I360(0, 180) & I360(75, 135)) + 180
            (I360(180, 360, False, False) & I360(255, 315, False, False))
        """
        return IIntersect(*[x + number for x in self.intervals])



class IUnion(IOperand):
    """Class for containing multiple intervals in a union
    """

    def __init__(self, *intervals) -> None:
        """Initialising an interval union

        Examples:
            >>> IUnion(I360(0, 90), I360(60, 120), I360(90, 120))
            (I360(0, 90) | I360(60, 120) | I360(90, 120))
        """
        ## Intervals that are a part of a union
        self.intervals = intervals
        super().__init__()
    
    def __contains__(self, number: int|float) -> bool:
        """Checking whether a number is within this interval union

        Args:
            number (int | float): Number value to check

        Returns:
            bool: True if the number is within at least one of the intervals
        
        Examples:
            >>> 60 in I360(0, 180) | I360(75, 135)
            True
            >>> 200 in I360(0, 180) | I360(75, 135)
            False
        """
        for interval in self.intervals:
            if number in interval:
                return True
        return False
    
    def __invert__(self) -> "IIntersect":
        """Inverts a union of intervals

        Returns:
            IIntersect: Intersection of inverted intervals
        
        Examples:
            >>> ~(I360(0, 180) | I360(75, 135))
            (I360(180, 360, True, True) & (I360(135, 360, True) | I360(0, 75, False, True)))
        """
        return IIntersect(*[~i for i in self.intervals])
    
    def __repr__(self) -> str:
        """Getting string representation of an interval union

        Returns:
            str: String representation
        
        Examples:
            >>> repr(I360(0, 180) | I360(75, 135))
            '(I360(0, 180) | I360(75, 135))'
        """
        return "(" + " | ".join((str(x) for x in self.intervals)) + ")"
    
    def __iter__(self) -> list:
        """Generating values from an interval union
        
        Examples:
            >>> list((I360(0, 180, points=8) | I360(75, 135, points=8)))
            [0.0, 45.0, 90.0, 135.0, 180.0]
            >>> list((I360(0, 60, points=16) | I360(90, 135, points=16)))
            [0.0, 22.5, 45.0, 90.0, 112.5, 135.0]
        """
        values = []
        for interval in self.intervals:
            for x in interval:
                if x not in values:
                    values.append(x)
        return iter(values)
    
    def __add__(self, number: int|float) -> "IUnion":
        """Incrementing a union of intervals

        Args:
            number (int | float): Number to increment by

        Returns:
            IUnion: Incremented interval union
        
        Examples:
            >>> (I360(0, 180) | I360(75, 135)) + 90
            (I360(90, 270, False, False) | I360(165, 225, False, False))
        """
        return IUnion(*[x + number for x in self.intervals])



@addInitRepr
@addCopyCall("start", "end", "openStart", "openEnd")
class I360(IOperand):
    """Class for representing a circular interval from 0 to 360 degrees

    This class is made immutable and has automatic __repr__ and __call__ using decorators.
    """

    ## \note Removal of the IUnion wrapper would result in I360.__init__ being called twice, which addInitRepr decorator does not allow
    def __new__(cls, start: int|float = 0, end: int|float = 360, openStart: bool = False, openEnd: bool = False, points: int = 8) -> "IOperand":
        """Creating a new instance by clamping passed values

        Args:
            start (int | float, optional): Start valie. Defaults to 0.
            end (int | float, optional): End value. Defaults to 360.
            openStart (bool, optional): Should the start of the interval be open? Defaults to False.
            openEnd (bool, optional): Should the end of the interval be open? Defaults to False.
            points (int, optional): Point count in a circle. Defaults to 8.

        Returns:
            IOperand: Either a I360 instance or a union of them
        
        Examples:
            >>> I360(-30, 30)
            (I360(330, 360, False, True) | I360(0, 30, False, False))
            >>> I360(0, 90)
            I360(0, 90)
            >>> I360(450, 630)
            (I360(90, 270, False, False))
        """
        if 0 <= start <= end <= 360:
            return super().__new__(cls)
        start, end = (x if 0 <= x <= 360 else x % 360 for x in (start, end))
        if start < end:
            return IUnion(I360(start, end, openStart, openEnd, points))
        return I360(start, 360, openStart, True, points) | I360(0, end, False, openEnd, points)
        

    def __init__(self, start: int|float = 0, end: int|float = 360, openStart: bool = False, openEnd: bool = False, points: int = 8) -> None:
        """Initialising a circular interval

        Args:
            start (int | float, optional): Start value. Defaults to 0.
            end (int | float, optional): End value. Defaults to 360.
            openStart (bool, optional): Should the start of the interval be open? Defaults to False.
            openEnd (bool, optional): Should the end of the interval be open? Defaults to False.
            points (int, optional): Point count in a circle. Defaults to 8.
        
        Examples:
            >>> I360(0, 90)
            I360(0, 90)
            >>> I360(120, 240, True, True)
            I360(120, 240, True, True)
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
        assert points > 0, "Point count has to be a positive number"
        ## Point count
        self.points = points
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
        
        Examples:
            >>> 90 in I360(0, 90)
            True
            >>> 90 in I360(0, 90, openEnd=True)
            False
            >>> 180 in I360(0, 90)
            False
        """
        if self.isEmpty:
            return False
        if number == self.start and not self.openStart:
            return True
        if number == self.end and not self.openEnd:
            if self.isFull:
                return self.openEnd
            return True
        return self.start < number < self.end
    
    def __invert__(self) -> "IOperand":
        """Inverting current interval

        Returns:
            IOperand: An interval that covers the rest of the circle
        
        Examples:
            >>> ~I360(60, 180)
            (I360(180, 360, True) | I360(0, 60, False, True))
            >>> ~I360(0, 120)
            I360(120, 360, True, True)
        """
        if self.isEmpty:
            return I360(0, 360, False, False, self.points)
        if self.isFull:
            return I360(0, 0, True, True, self.points)
        if self.start == 0:
            return I360(self.end, 360, not self.openEnd, not self.openStart, self.points)
        if self.end == 360:
            return I360(0, self.start, not self.openEnd, not self.openStart, self.points)
        return I360(self.end, 360, not self.openEnd, self.points) | I360(0, self.start, False, not self.openStart, self.points)
    
    def __iter__(self):
        """Generating angles that belong to the interval
        
        Examples:
            >>> list(I360(0, 90, points=16))
            [0.0, 22.5, 45.0, 67.5, 90.0]
            >>> list(I360(0, 180, True, points=6))
            [60.0, 120.0, 180.0]
            >>> list(I360(openEnd=True, points=4))
            [0.0, 90.0, 180.0, 270.0]
        """
        for i in range(self.points + 1):
            angle = 360 * i / self.points
            if angle in self:
                yield angle % 360
    
    def __add__(self, number: int|float) -> "IOperand":
        """Incrementing a circular interval

        Args:
            number (int | float): Number to increment by

        Returns:
            IOperand: Either a I360 instance or a union of them
        
        Examples:
            >>> I360(0, 120) + 180
            I360(180, 300, False, False)
            >>> I360(300, 330) + 120
            I360(60, 90, False, False)
        """
        if self.isEmpty or self.isFull:
            return self
        return I360(self.start + number, self.end + number, self.openStart, self.openEnd, self.points)



## An empty interval, equals to I360(0, 0, True, True)
I360.EMPTY = I360(0, 0, True, True)
## A full interval, equals to I360(0, 360, False, False)
I360.FULL = I360(0, 360)
## Interval corresponding to the first half of a circle
I360.HALF1 = I360(0, 180)
## Interval corresponding to the second half of a circle
I360.HALF2 = I360(180, 360)
## Interval corresponding to the first quarter of a circle
I360.QUARTER1 = I360(0, 90)
## Interval corresponding to the second quarter of a circle
I360.QUARTER2 = I360(90, 180)
## Interval corresponding to the third quarter of a circle
I360.QUARTER3 = I360(180, 270)
## Interval corresponding to the fourth quarter of a circle
I360.QUARTER4 = I360(270, 360)