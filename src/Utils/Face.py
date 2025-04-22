## \file
# Class for representing a single face of an Object
from .Decorators import makeImmutable, addInitRepr, addCopyCall
from .Line import Line
from .Vector import V3
from typing import Iterator


# noinspection PyCallingNonCallable
@makeImmutable
@addInitRepr
@addCopyCall("points")
class Face:
    """Class for representing a face
    """

    def __init__(self, points: tuple) -> None:
        """Initializing a Face instance
        """
        ## Vertices making up the face
        if len(points) < 3:
            raise ValueError("Face must have at least 3 vertices")
        if len(points) != len(set(points)):
            raise ValueError("Face cannot have duplicate vertices")
        self.points = points

    def __iter__(self) -> Iterator[Line]:
        """Iterating over face edges
        """
        for i in range(len(self.points)):
            yield Line(self.points[i - 1], self.points[i])

    def __eq__(self, other: "Face") -> bool:
        """Comparing two faces

        Args:
            other (Face): The other face

        Returns:
            bool: True if the two faces are equal
        """
        if not isinstance(other, self.__class__):
            return False
        return set(self) == set(other)

    def __hash__(self) -> int:
        """Hashing lines making up the face

        Returns:
            int: Hash code
        """
        return hash(frozenset(self))

    def __add__(self, other: V3) -> "Face":
        """Incrementing face bounds by a vector

        Args:
            other (V3): Vector to increment face bounds by

        Returns:
            Face: Incremented face
        """
        return self(tuple(point + other for point in self.points))

    def __rshift__(self, other: float) -> "Face":
        """Rotating a face by an amount of degrees

        Args:
            other (float): Angle to rotate face by

        Returns:
            Face: Rotated face
        """
        return self(tuple(point >> other for point in self.points))