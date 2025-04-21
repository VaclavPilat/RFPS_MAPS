## \file
# Class for representing a line between two points
from .Decorators import makeImmutable, addInitRepr
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
        if not isinstance(other, Line):
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