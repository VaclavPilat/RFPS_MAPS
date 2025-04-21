## \file
# Class for representing a single face of an Object
from .Decorators import makeImmutable, addInitRepr
from .Line import Line
from .Vector import V3
from typing import Iterator


@makeImmutable
@addInitRepr
class Face:
    """Class for representing a face
    """

    def __init__(self, *points: V3) -> None:
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
            yield Line(*self.points[i - 1:i + 1])