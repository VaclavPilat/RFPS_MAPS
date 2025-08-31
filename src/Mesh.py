"""! \file
Classes for representing mesh structure.

Mesh data is stored in Object instances (recursive tree-like structures).
Each Object may contain multiple Face objects.
Face instances are represented by Line objects.
Each Line is represented by 2 Vector points.

\todo Use Decimal everywhere with float trap set to True (but leave Vector without type restrictions)
\todo Add multiple axis rotation: `Vector >> Vector`

\internal
Examples:
    >>> Line(ZERO, UP) | Line(RIGHT, RIGHT+DOWN)
    True
"""
from .Decorators import *
import math


@addOperators
@addInitRepr
@makeImmutable
@addCopyCall("x", "y", "z")
class Vector:
    """Class for representing a 3D vector.

    The X axis is for forward/backward values, Y is for left/right and Z is for vertical values.

    Examples:
        >>> Vector(1, 2, 3)
        Vector(1, 2, 3)
        >>> Vector(z=3)
        Vector(z=3)
    """

    def __init__(self, x: int|float = 0, y: int|float = 0, z: int|float = 0) -> None:
        """Initializing a 3D vector

        Args:
            x (int | float, optional): X value. Defaults to 0.
            y (int | float, optional): Y value. Defaults to 0.
            z (int | float, optional): Z value. Defaults to 0.
        """
        ## Value of the X axis
        self.x = x
        ## Value of the Y axis
        self.y = y
        ## Value of the Z axis
        self.z = z

    def __iter__(self):
        """Iterating over values

        Returns:
            Iterator representing vector values

        Examples:
            >>> list(Vector(1, 2, 3)) == list(Vector(1, 2, 3))
            True
            >>> list(Vector(1, 2, 3)) == list(Vector(1, 2, 2))
            False
        """
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        """Getting the hash of this vector

        Returns:
            Hash representation of this vector

        Examples:
            >>> hash(Vector(1, 2, 3)) == hash(Vector(1, 2, 3))
            True
            >>> hash(Vector(1, 2, 3)) == hash(Vector(0, 2, 3))
            False
        """
        return hash(tuple(self))

    def __eq__(self, other: "Vector") -> bool:
        """Comparing this vector to another one

        Args:
            other (Vector): Other vector

        Returns:
            bool: True if both have the same values

        Examples:
            >>> Vector(1, 2, 3) == Vector(1, 2, 3)
            True
            >>> Vector(1, 2, 3) == Vector(1, 3, 2)
            False
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neg__(self) -> "Vector":
        """Negating this vector

        Returns:
            Vector: Vector with negated axis values

        Examples:
            >>> -Vector(3, -5, 8) == Vector(-3, 5, -8)
            True
        """
        return Vector(-self.x, -self.y, -self.z)

    def __add__(self, other: "Vector") -> "Vector":
        """Adding two vectors together

        Args:
            other (Vector): Other vector

        Returns:
            Vector: Sum of this and the other vector

        Examples:
            >>> Vector(1, 2, 3) + Vector(-5, 8, 14) == Vector(-4, 10, 17)
            True
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return Vector(*(a + b for a, b in zip(self, other)))

    def __mul__(self, other: int|float) -> "Vector":
        """Multiplication of a vector by a number

        Args:
            other (int | float): Number to multiply by

        Returns:
            Vector: Product of this vector and the number

        Examples:
            >>> Vector(1, 2, 3) * 0 == Vector(0, 0, 0)
            True
            >>> Vector(1, 2, 3) * 1 == Vector(1, 2, 3)
            True
            >>> Vector(1, 2, 3) * 2 == Vector(2, 4, 6)
            True
        """
        return Vector(*(other * a for a in self))

    def __truediv__(self, other: int | float) -> "Vector":
        """Division of a vector by a number

        Args:
            other (int | float): Number to divide by

        Returns:
            Vector: Quotient of this vector and the number

        Examples:
            >>> Vector(1, 2, 3) / 1 == Vector(1, 2, 3)
            True
            >>> Vector(1, 2, 3) / 2 == Vector(0.5, 1, 1.5)
            True
        """
        return Vector(*(a / other for a in self))

    def __rshift__(self, other: int|float) -> "Vector":
        """Rotating the vector on Z axis, clockwise

        Args:
            other (int|float): Rotation angle in degrees

        Returns:
            Vector: Rotated vector

        Examples:
            >>> Vector(1, 2, 3) >> 0 == Vector(1, 2, 3)
            True
            >>> Vector(1, 2, 3) >> 90 == Vector(2, -1, 3)
            True
            >>> Vector(1, 2, 3) >> 180 == Vector(-1, -2, 3)
            True
            >>> Vector(1, 2, 3) >> 270 == Vector(-2, 1, 3)
            True
        """
        if other % 90 != 0:
            return NotImplemented
        other %= 360
        if other == 90:
            return Vector(self.y, -self.x, self.z)
        if other == 180:
            return Vector(-self.x, -self.y, self.z)
        if other == 270:
            return Vector(-self.y, self.x, self.z)
        return self

    def __abs__(self) -> float:
        """Calculating the magnitude of the vector

        Returns:
            float: Magnitude of a vector

        Examples:
            >>> abs(Vector()) == 0
            True
            >>> abs(Vector(3, 4, 0)) == 5
            True
            >>> abs(Vector(z=10)) == 10
            True
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __matmul__(self, other: "Vector") -> "Vector":
        """Calculating the cross product of two vectors

        Args:
            other (Vector): Other vector

        Returns:
            Vector: Cross product of two vectors

        Examples:
            >>> Vector(1, 2, 3) @ Vector(1, 2, 3) == Vector(0, 0, 0)
            True
            >>> Vector(1, 2, 3) @ Vector(4, 5, 6) == Vector(-3, 6, -3)
            True
            >>> Vector(1, 2, 3) @ Vector(-1, -2, -3) == Vector(0, 0, 0)
            True
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __bool__(self) -> bool:
        """Checking whether the vector is non-zero

        Returns:
            bool: True if the vector is not equal to Vector(0, 0, 0)

        Examples:
            >>> bool(Vector(1, 2, 3))
            True
            >>> bool(Vector(0, 1, 0))
            True
            >>> bool(Vector(0, 0, 0))
            False
        """
        return self.x != 0 or self.y != 0 or self.z != 0


@addOperators
@makeImmutable
@addInitRepr
class Line:
    """A line between two points.

    It is defined as a set of 2 vertices (since it does not have a direction).

    Examples:
        >>> Line(ZERO, ZERO)
        Traceback (most recent call last):
        ValueError: Points must be different
    """

    def __init__(self, a: Vector, b: Vector) -> None:
        """Initialize a line.

        Args:
            a (Vector): First point of the line.
            b (Vector): Second point of the line.
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

        Examples:
            >>> Line(ZERO, ONE) == Line(ZERO, ONE)
            True
            >>> Line(ZERO, ONE) == Line(ONE, ZERO)
            True
            >>> Line(ZERO, ONE) == Line(ONE, LEFT)
            False
        """
        if not isinstance(other, self.__class__):
            return False
        return (self.a == other.a and self.b == other.b) or (self.a == other.b and self.b == other.a)

    def __hash__(self) -> int:
        """Hashing a line instance.

        Returns:
            int: The hash value of the instance.

        Examples:
            >>> hash(Line(ZERO, ONE)) == hash(Line(ONE, ZERO))
            True
            >>> hash(Line(ZERO, ONE)) == hash(Line(ONE, LEFT))
            False
        """
        return hash(frozenset((self.a, self.b)))

    def __call__(self, *args, **kwargs) -> "Line":
        """Making a copy of a line with altered arguments.

        Returns:
            Line: A copy of the line with altered params.

        Examples:
            >>> Line(LEFT, RIGHT)() == Line(LEFT, RIGHT)
            True
            >>> Line(ONE, UP)(z=0) == Line(Vector(x=1, y=1, z=0), Vector(x=0, y=0, z=0))
            True
        """
        # noinspection PyCallingNonCallable
        return Line(self.a(*args, **kwargs), self.b(*args, **kwargs))

    def __iter__(self):
        """Iterating over line bounds

        Examples:
            >>> list(Line(LEFT, RIGHT)) == [LEFT, RIGHT]
            True
        """
        yield self.a
        yield self.b

    def __add__(self, other: Vector) -> "Line":
        """Incrementing line bounds by a vector

        Args:
            other (Vector): Vector to add

        Returns:
            Line: A copy of the line with offset line bounds.

        Examples:
            >>> Line(ONE, UP) + UP == Line(Vector(1, 1, 2), Vector(0, 0, 2))
            True
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return Line(*(point + other for point in self))

    def __rshift__(self, other: int|float) -> "Line":
        """Rotating a line by a vector

        Args:
            other (int | float): Angle to rotate by

        Returns:
            Line: A copy of the line with rotated line bounds.

        Examples:
            >>> Line(FORWARD, LEFT) >> 90 == Line(RIGHT, FORWARD)
            True
        """
        return Line(*(point >> other for point in self))

    def __or__(self, other: "Line") -> bool:
        """Checking whether both lines are in parallel

        Args:
            other (Line): Other line

        Returns:
            bool: True if both lines are in parallel

        Examples:
            >>> Line(ZERO, ONE) | Line(ZERO, ONE)
            True
            >>> Line(ZERO, ONE) | Line(UP, ONE + UP)
            True
            >>> Line(ZERO, ONE) | Line(UP, RIGHT)
            False
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        # noinspection PyUnresolvedReferences
        return not (self.a - self.b) @ (other.a - other.b)


@makeImmutable
@addInitRepr
class Face:
    """Class for representing a face

    Examples:
        >>> Face(ZERO, RIGHT)
        Traceback (most recent call last):
        ValueError: Face must have at least 3 vertices
        >>> Face(ZERO, LEFT, ZERO)
        Traceback (most recent call last):
        ValueError: Face cannot have duplicate vertices
    """

    def __init__(self, *points) -> None:
        """Initializing a Face instance
        """
        ## Vertices making up the face
        if len(points) < 3:
            raise ValueError("Face must have at least 3 vertices")
        if len(points) != len(set(points)):
            raise ValueError("Face cannot have duplicate vertices")
        self.points = points

    def __iter__(self):
        """Iterating over face edges (lines)

        Examples:
            >>> tuple(Face(ZERO, ONE, UP)) == (Line(UP, ZERO), Line(ZERO, ONE), Line(ONE, UP))
            True
        """
        for i in range(len(self.points)):
            yield Line(self.points[i - 1], self.points[i])

    def __len__(self) -> int:
        """Getting vertex count

        Returns:
            int: Number of vertices that define this face
        """
        return len(self.points)

    def __eq__(self, other: "Face") -> bool:
        """Comparing the vertices that make up the face and its direction.

        Comparison is done by "rotating" the sequence of vertices until it matches the other Face.
        The "order" of face vertices matters - clockwise or counterclockwise affect the face direction.

        Args:
            other (Face): The other face

        Returns:
            bool: True if the two faces are equal

        Examples:
            >>> Face(ZERO, ONE, UP) == Face(ZERO, ONE, UP)
            True
            >>> Face(ZERO, ONE, UP) == Face(ONE, UP, ZERO)
            True
            >>> Face(ZERO, ONE, UP) == Face(ZERO, UP, ONE)
            False
            >>> Face(ZERO, UP, ONE) == Face(ZERO, UP, DOWN)
            False
        """
        if not isinstance(other, self.__class__) or len(self) != len(other):
            return False
        for i in range(len(self)):
            if self.points[i:] + self.points[:i] == other.points:
                return True
        return False

    def __hash__(self) -> int:
        """Hashing lines making up the face.

        Return value is a hash of the rotated (normalized) sequnce of points.

        Returns:
            int: Hash code

        Examples:
            >>> hash(Face(ZERO, ONE, UP)) == hash(Face(ZERO, ONE, UP))
            True
            >>> hash(Face(ZERO, ONE, UP)) == hash(Face(ONE, UP, ZERO))
            True
            >>> hash(Face(ZERO, ONE, UP)) == hash(Face(ZERO, UP, ONE))
            False
            >>> hash(Face(ZERO, UP, ONE)) == hash(Face(ZERO, UP, DOWN))
            False
        """
        hashes = tuple(hash(point) for point in self.points)
        index = hashes.index(min(hashes))
        return hash(hashes[index:] + hashes[:index])

    def __add__(self, other: Vector) -> "Face":
        """Incrementing face bounds by a vector

        Args:
            other (Vector): Vector to increment face bounds by

        Returns:
            Face: Incremented face

        Examples:
            >>> Face(ZERO, ONE, UP) + ZERO == Face(ZERO, ONE, UP)
            True
            >>> Face(ZERO, ONE, UP) + DOWN == Face(DOWN, ONE + DOWN, ZERO)
            True
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return Face(*(point + other for point in self.points))

    def __rshift__(self, other: int|float) -> "Face":
        """Rotating a face by an amount of degrees

        Args:
            other (int | float): Angle to rotate face by

        Returns:
            Face: Rotated face

        Examples:
            >>> Face(ZERO, ONE, UP) >> 0 == Face(ZERO, ONE, UP)
            True
            >>> Face(ZERO, FORWARD, RIGHT) >> 90 == Face(ZERO, RIGHT, BACKWARD)
            True
        """
        return Face(*(point >> other for point in self.points))


## Zero-filled vector, equals to Vector(0, 0, 0)
ZERO = Vector()
## One-filled vector, equals to Vector(1, 1, 1)
ONE = Vector(1, 1, 1)
## Forward direction vector, equals to Vector(1, 0, 0)
FORWARD = Vector(x=1)
## Backward direction vector, equals to Vector(-1, 0, 0)
BACKWARD = Vector(x=-1)
## Left direction vector, equals to Vector(0, 1, 0)
LEFT = Vector(y=1)
## Right direction vector, equals to Vector(0, -1, 0)
RIGHT = Vector(y=-1)
## Up direction vector, equals to Vector(0, 0, 1)
UP = Vector(z=1)
## Down direction vector, equals to Vector(0, 0, -1)
DOWN = Vector(z=-1)