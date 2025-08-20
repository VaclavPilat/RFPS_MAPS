## \file
# Implementation of circular intervals
from . import Decorators


@Decorators.makeImmutable
@Decorators.addInitRepr
@Decorators.addCopyCall()
class I360:
    """Class for generating values from within an interval.
    """

    def __init__(self, start: int = 0, end: int = 360, includeStart: bool = True, includeEnd: bool = True):
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

    def __contains__(self, item: int) -> bool:
        """Checking whether a number is a part of the interval.

        Args:
            item (int): The number to check.

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