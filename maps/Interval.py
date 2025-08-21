## \file
# Implementation of circular intervals
from . import Decorators


class Interval:
    """Base inteval class with common operations.
    """

    def __and__(self, other: "Interval") -> "Intersection":
        """Creating an intersetion of intervals

        Args:
            other (Interval): The other interval

        Returns:
            Intersection: Created interval intersection
        """
        return Intersection(self, other)

    def __or__(self, other: "Interval") -> "Union":
        """Creating a union of intervals

        Args:
            other (Interval): The other interval

        Returns:
            Union: Created interval union
        """
        return Union(self, other)


@Decorators.makeImmutable
@Decorators.addInitRepr
class Union(Interval):
    """Class for representing a union of intervals.
    """

    def __init__(self, *intervals) -> None:
        """Initialising a union of intervals.

        Args:
            *intervals: Interval arguments.
        """
        ## Tuple of interval arguments
        self.intervals = intervals

    def __contains__(self, item: int|float) -> bool:
        """Checking whether an item is contained in this Union.

        Args:
            item (int | float): Item to check.

        Returns:
            bool: True if ANY interval contains this item.

        Examples:
            >>> 300 in Union(I360(0, 180), I360(90, 270))
            False
            >>> 60 in Union(I360(0, 180), I360(90, 270))
            True
            >>> 200 in Union(I360(0, 180), I360(90, 270))
            True
            >>> 120 in Union(I360(0, 180), I360(90, 270))
            True
        """
        return any(item in interval for interval in self.intervals)


@Decorators.makeImmutable
@Decorators.addInitRepr
class Intersection(Interval):
    """Class for representing an intersection of intervals.
    """

    def __init__(self, *intervals) -> None:
        """Initialising an intersection of intervals.

        Args:
            *intervals: Interval arguments.
        """
        ## Tuple of interval arguments
        self.intervals = intervals

    def __contains__(self, item: int|float) -> bool:
        """Checking whether an item is contained in this Intersection.

        Args:
            item (int | float): Item to check.

        Returns:
            bool: True if ALL intervals contains this item.

        Examples:
            >>> 300 in Intersection(I360(0, 180), I360(90, 270))
            False
            >>> 60 in Intersection(I360(0, 180), I360(90, 270))
            False
            >>> 200 in Intersection(I360(0, 180), I360(90, 270))
            False
            >>> 120 in Intersection(I360(0, 180), I360(90, 270))
            True
        """
        return all(item in interval for interval in self.intervals)


@Decorators.makeImmutable
@Decorators.addInitRepr
@Decorators.addCopyCall()
class I360(Interval):
    """Class for generating values from within an interval.
    """

    def __init__(self, start: int = 0, end: int = 360, includeStart: bool = True, includeEnd: bool = True) -> None:
        """Initialising a circular interval.

        Args:
            start (int, optional): The starting angle of the interval. Defaults to 0.
            end (int, optional): The ending angle of the interval. Defaults to 360.
            includeStart (bool, optional): If True, include the start of the interval. Defaults to True.
            includeEnd (bool, optional): If True, include the end of the interval. Defaults to True.
        """
        if start > end:
            raise ValueError("Start angle cannot be greater than end angle.")
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
            >>> 0 in I360()
            True
            >>> 360 in I360()
            True
            >>> 270 in I360(end=180)
            False
            >>> 180 in I360(0, 180, True, False)
            False
        """
        return (self.start <= item if self.includeStart else self.start < item) \
            and (item <= self.end if self.includeEnd else item < self.end)


I360.FULL = I360()
I360.EMPTY = I360(0, 0, False, False)


if __name__ == '__main__':
    from . import Helpers
    Helpers.doctests()