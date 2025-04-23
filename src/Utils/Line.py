## \file
# Class for representing a line between two points
from .Decorators import makeImmutable, addInitRepr, addCopyCall
from .Vector import V3
from typing import Iterator


@makeImmutable
@addInitRepr
class Line:
    """A line connecting two points.
    """

    def __init__(self, a: V3, b: V3) -> None:
        """Initialize a line.

        Args:
            a (V3): First point of the line.
            b (V3): Second point of the line.
        """
        if a == b:
            raise ValueError("Points must be different")
        ## First point
        self.a = a
        ## Second point
        self.b = b

    def __eq__(self, other: "Line") -> bool:
        """Checking line equality

        Returns:
            bool: True if the line is equal to the other line.
        """
        if not isinstance(other, self.__class__):
            return False
        return (self.a == other.a and self.b == other.b) or (self.a == other.b and self.b == other.a)

    def __hash__(self) -> int:
        """Hashing a line instance.

        Returns:
            int: The hash value of the instance.
        """
        return hash(frozenset((self.a, self.b)))

    def __call__(self, *args, **kwargs) -> "Line":
        """Making a copy of a line.

        Returns:
            Line: A copy of the line with altered params.
        """
        # noinspection PyCallingNonCallable
        return Line(self.a(*args, **kwargs), self.b(*args, **kwargs))

    def __iter__(self) -> Iterator[V3]:
        """Iterating over line points
        """
        yield self.a
        yield self.b

    def __add__(self, other: V3) -> "Line":
        """Adding a vector to the line

        Args:
            other (V3): Vector to add

        Returns:
            Line: A copy of the line with offset line bounds.
        """
        return self(*(point + other for point in self))

    def __rshift__(self, other: float) -> "Line":
        """Rotating a line by a vector

        Args:
            other (float): Angle to rotate by

        Returns:
            Line: A copy of the line with rotated line bounds.
        """
        return self(*(point >> other for point in self))

    ## \note This method only supports comparisons between lines that are parallel to axis.
    def __contains__(self, item: "Line") -> bool:
        """Checking whether a line is contained by this one.

        Args:
            item (Line): Line to check

        Returns:
            bool: True if the line is contained by this one.
        """