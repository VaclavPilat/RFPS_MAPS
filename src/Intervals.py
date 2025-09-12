"""! \file
Implementation of circular intervals

\internal
Examples:
    >>> list(EMPTY[8])
    []
    >>> list((HALF1 | HALF2)[8]) == list(FULL[8])
    True
"""
from .Decorators import makeImmutable, addInitRepr, addCopyCall


class Interval:
    """Base inteval class with common operations.
    """

    def __and__(self, other: "Interval") -> "Intersection":
        """Creating an intersetion of intervals

        Args:
            other (Interval): The other interval

        Returns:
            Intersection: Created interval intersection

        Examples:
            >>> list((Arc(0, 180) & Arc(90, 270))[8])
            [90.0, 135.0, 180.0]
        """
        return Intersection(self, other)

    def __or__(self, other: "Interval") -> "Union":
        """Creating a union of intervals

        Args:
            other (Interval): The other interval

        Returns:
            Union: Created interval union

        Examples:
            >>> list((Arc(0, 180) | Arc(90, 270))[8])
            [0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0]
        """
        return Union(self, other)


@makeImmutable
@addInitRepr
class Union(Interval):
    """Class for representing a union of intervals.

    Examples:
        >>> Union()
        Traceback (most recent call last):
        ValueError: Union cannot be empty
    """

    def __init__(self, *intervals) -> None:
        """Initialising a union of intervals.

        Args:
            *intervals: Interval arguments.
        """
        if len(intervals) < 2:
            raise ValueError("Union cannot be empty")
        ## Tuple of interval arguments
        self.intervals = intervals

    def __contains__(self, item: int|float) -> bool:
        """Checking whether an item is contained in this Union.

        Args:
            item (int | float): Item to check.

        Returns:
            bool: True if ANY interval contains this item.

        Examples:
            >>> 300 in Union(Arc(0, 180), Arc(90, 270))
            False
            >>> 60 in Union(Arc(0, 180), Arc(90, 270))
            True
            >>> 200 in Union(Arc(0, 180), Arc(90, 270))
            True
            >>> 120 in Union(Arc(0, 180), Arc(90, 270))
            True
        """
        return any(item in interval for interval in self.intervals)

    def __getitem__(self, points: int):
        """Generating angle values that belong to an interval Union.

        Args:
            points (int): Number of points on the WHOLE CIRCLE

        Yields:
            float: Angle value in degrees belonging to the interval

        Examples:

        """
        for angle in FULL[points]:
            if any(angle in interval[points] for interval in self.intervals):
                yield angle


@makeImmutable
@addInitRepr
class Intersection(Interval):
    """Class for representing an intersection of intervals.

    Examples:
        >>> Intersection()
        Traceback (most recent call last):
        ValueError: Intersection cannot be empty
    """

    def __init__(self, *intervals) -> None:
        """Initialising an intersection of intervals.

        Args:
            *intervals: Interval arguments.
        """
        if len(intervals) == 0:
            raise ValueError("Intersection cannot be empty")
        ## Tuple of interval arguments
        self.intervals = intervals

    def __contains__(self, item: int|float) -> bool:
        """Checking whether an item is contained in this Intersection.

        Args:
            item (int | float): Item to check.

        Returns:
            bool: True if ALL intervals contains this item.

        Examples:
            >>> 300 in Intersection(Arc(0, 180), Arc(90, 270))
            False
            >>> 60 in Intersection(Arc(0, 180), Arc(90, 270))
            False
            >>> 200 in Intersection(Arc(0, 180), Arc(90, 270))
            False
            >>> 120 in Intersection(Arc(0, 180), Arc(90, 270))
            True
        """
        return all(item in interval for interval in self.intervals)

    def __getitem__(self, points: int):
        """Generating angle values that belong to an interval Intersection.

        Args:
            points (int): Number of points on the WHOLE CIRCLE

        Yields:
            float: Angle value in degrees belonging to the interval

        Examples:

        """
        for angle in FULL[points]:
            if all(angle in interval[points] for interval in self.intervals):
                yield angle


@makeImmutable
@addInitRepr
@addCopyCall("start", "end", "includeStart", "includeEnd")
class Arc(Interval):
    """Class for generating values from within an interval.

    Examples:
        >>> Arc()
        Arc()
        >>> Arc()(end=180)
        Arc(start=0, end=180, includeStart=True, includeEnd=True)
    """

    def __new__(cls, start: int = 0, end: int = 360, includeStart: bool = True, includeEnd: bool = True) -> Interval:
        """Creating a new interval by clamping its arguments

        Args:
            start (int, optional): The starting angle of the interval. Defaults to 0.
            end (int, optional): The ending angle of the interval. Defaults to 360.
            includeStart (bool, optional): If True, include the start of the interval. Defaults to True.
            includeEnd (bool, optional): If True, include the end of the interval. Defaults to True.

        Returns:
            Interval: Either an Arc instance or a union of them

        Examples:
            >>> 100 in Arc(90, 180)
            True
            >>> 60 in Arc(-90, 90)
            True
            >>> 180 in Arc(-30, 30)
            False
            >>> 360 in Arc(270, 90)
            True
        """
        if 0 <= start <= end <= 360:
            return super().__new__(cls)
        start, end = (x if 0 <= x <= 360 else x % 360 for x in (start, end))
        if start < end:
            return Union(Arc(start, end, includeStart, includeEnd))
        return Arc(start, 360, includeStart, True) | Arc(0, end, False, includeEnd)

    def __init__(self, start: int = 0, end: int = 360, includeStart: bool = True, includeEnd: bool = True) -> None:
        """Initialising a circular interval.

        Args:
            start (int, optional): The starting angle of the interval. Defaults to 0.
            end (int, optional): The ending angle of the interval. Defaults to 360.
            includeStart (bool, optional): If True, include the start of the interval. Defaults to True.
            includeEnd (bool, optional): If True, include the end of the interval. Defaults to True.
        """
        if not (0 <= start <= end <= 360):
            raise ValueError("Invalid angle bound values.")
        ## Start value of the interval
        self.start = start
        ## End value of the interval
        self.end = end
        ## Include the starting value?
        self.includeStart = includeStart
        ## Include the ending value?
        self.includeEnd = includeEnd

    def __contains__(self, item: int|float) -> bool:
        """Checking whether a number is a part of the interval.

        Args:
            item (int | float): The number to check.

        Returns:
            bool: Whether the number is a part of the interval.

        Examples:
            >>> 0 in Arc()
            True
            >>> 360 in Arc()
            True
            >>> 270 in Arc(end=180)
            False
            >>> 180 in Arc(0, 180, True, False)
            False
        """
        return (self.start <= item if self.includeStart else self.start < item) \
            and (item <= self.end if self.includeEnd else item < self.end)

    def __getitem__(self, points: int):
        """Generating angle values that belong to the interval.

        This is done by generating regular points on a WHOLE CIRCLE and yielding them if they belong to the interval.
        0 or 360 will be yielded only once regardless whether the interval represents a full circle.

        Args:
            points (int): Number of points on the WHOLE CIRCLE

        Yields:
            float: Angle value in degrees belonging to the interval

        Examples:
            >>> list(Arc()[0])
            Traceback (most recent call last):
            ValueError: Invalid point count.
            >>> list(Arc()[1])
            [0.0]
            >>> list(Arc()[3])
            [0.0, 120.0, 240.0]
            >>> list(Arc(includeStart=False)[3])
            [120.0, 240.0, 360.0]
        """
        if points <= 0:
            raise ValueError("Invalid point count.")
        for i in range(points + 1):
            angle = 360 * i / points
            if angle in self:
                if angle == 360 and 0 in self:
                    continue
                yield angle


FULL = Arc()
EMPTY = Arc(0, 0, False, False)
HALF1 = Arc(0, 180)
HALF2 = Arc(180, 360)