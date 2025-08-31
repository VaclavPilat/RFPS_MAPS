"""! \file
Classes for representing mesh structure.

Mesh data is stored in Object instances (a recursive tree-like structures).
Each Object may contain multiple Face objects.
Face instances are represented by Line objects.
Each Line is represented by 2 V3 points.

\todo Use Decimal everywhere with float trap set to True (but leave V3 without type restrictions)
\todo Add multiple axis rotation: `V3 >> V3`

\internal
Examples:
    >>> FORWARD >> 90 == RIGHT
    True
    >>> ONE * 0 == ZERO
    True
    >>> LEFT @ RIGHT == ZERO
    True
"""
from .Decorators import makeImmutable, addOperators, addInitRepr, addCopyCall
import math


@addOperators
@addInitRepr
@makeImmutable
@addCopyCall("x", "y", "z")
class V3:
    """Class for representing a 3D vector.

    The X axis is for forward/backward values, Y is for left/right and Z is for vertical values.

    Examples:
        >>> V3(1, 2, 3)
        V3(1, 2, 3)
        >>> V3(z=3)
        V3(z=3)
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
            >>> list(V3(1, 2, 3)) == list(V3(1, 2, 3))
            True
            >>> list(V3(1, 2, 3)) == list(V3(1, 2, 2))
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
            >>> hash(V3(1, 2, 3)) == hash(V3(1, 2, 3))
            True
            >>> hash(V3(1, 2, 3)) == hash(V3(0, 2, 3))
            False
        """
        return hash(tuple(self))

    def __eq__(self, other: "V3") -> bool:
        """Comparing this vector to another one

        Args:
            other (V3): Other vector

        Returns:
            bool: True if both have the same values

        Examples:
            >>> V3(1, 2, 3) == V3(1, 2, 3)
            True
            >>> V3(1, 2, 3) == V3(1, 3, 2)
            False
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neg__(self) -> "V3":
        """Negating this vector

        Returns:
            V3: Vector with negated axis values

        Examples:
            >>> -V3(3, -5, 8) == V3(-3, 5, -8)
            True
        """
        return V3(-self.x, -self.y, -self.z)

    def __add__(self, other: "V3") -> "V3":
        """Adding two vectors together

        Args:
            other (V3): Other vector

        Returns:
            V3: Sum of this and the other vector

        Examples:
            >>> V3(1, 2, 3) + V3(-5, 8, 14) == V3(-4, 10, 17)
            True
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return V3(*(a + b for a, b in zip(self, other)))

    def __mul__(self, other: int|float) -> "V3":
        """Multiplication of a vector by a number

        Args:
            other (int | float): Number to multiply by

        Returns:
            V3: Product of this vector and the number

        Examples:
            >>> V3(1, 2, 3) * 0 == V3(0, 0, 0)
            True
            >>> V3(1, 2, 3) * 1 == V3(1, 2, 3)
            True
            >>> V3(1, 2, 3) * 2 == V3(2, 4, 6)
            True
        """
        return V3(*(other * a for a in self))

    def __truediv__(self, other: int | float) -> "V3":
        """Division of a vector by a number

        Args:
            other (int | float): Number to divide by

        Returns:
            V3: Quotient of this vector and the number

        Examples:
            >>> V3(1, 2, 3) / 1 == V3(1, 2, 3)
            True
            >>> V3(1, 2, 3) / 2 == V3(0.5, 1, 1.5)
            True
        """
        return V3(*(a / other for a in self))

    def __rshift__(self, other: int|float) -> "V3":
        """Rotating the vector on Z axis, clockwise

        Args:
            other (int|float): Rotation angle in degrees

        Returns:
            V3: Rotated vector

        Examples:
            >>> V3(1, 2, 3) >> 0 == V3(1, 2, 3)
            True
            >>> V3(1, 2, 3) >> 90 == V3(2, -1, 3)
            True
            >>> V3(1, 2, 3) >> 180 == V3(-1, -2, 3)
            True
            >>> V3(1, 2, 3) >> 270 == V3(-2, 1, 3)
            True
        """
        if other % 90 != 0:
            return NotImplemented
        other %= 360
        if other == 90:
            return V3(self.y, -self.x, self.z)
        if other == 180:
            return V3(-self.x, -self.y, self.z)
        if other == 270:
            return V3(-self.y, self.x, self.z)
        return self

    def __abs__(self) -> float:
        """Calculating the magnitude of the vector

        Returns:
            float: Magnitude of a vector

        Examples:
            >>> abs(V3()) == 0
            True
            >>> abs(V3(3, 4, 0)) == 5
            True
            >>> abs(V3(z=10)) == 10
            True
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __matmul__(self, other: "V3") -> "V3":
        """Calculating the cross product of two vectors

        Args:
            other (V3): Other vector

        Returns:
            V3: Cross product of two vectors

        Examples:
            >>> V3(1, 2, 3) @ V3(1, 2, 3) == V3(0, 0, 0)
            True
            >>> V3(1, 2, 3) @ V3(4, 5, 6) == V3(-3, 6, -3)
            True
            >>> V3(1, 2, 3) @ V3(-1, -2, -3) == V3(0, 0, 0)
            True
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return V3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __bool__(self) -> bool:
        """Checking whether the vector is non-zero

        Returns:
            bool: True if the vector is not equal to V3(0, 0, 0)

        Examples:
            >>> bool(V3(1, 2, 3))
            True
            >>> bool(V3(0, 1, 0))
            True
            >>> bool(V3(0, 0, 0))
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
            >>> Line(ONE, UP)(z=0) == Line(V3(x=1, y=1, z=0), V3(x=0, y=0, z=0))
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

    def __add__(self, other: V3) -> "Line":
        """Incrementing line bounds by a vector

        Args:
            other (V3): Vector to add

        Returns:
            Line: A copy of the line with offset line bounds.

        Examples:
            >>> Line(ONE, UP) + UP == Line(V3(1, 1, 2), V3(0, 0, 2))
            True
        """
        if not isinstance(other, V3):
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

    def __add__(self, other: V3) -> "Face":
        """Incrementing face bounds by a vector

        Args:
            other (V3): Vector to increment face bounds by

        Returns:
            Face: Incremented face

        Examples:
            >>> Face(ZERO, ONE, UP) + ZERO == Face(ZERO, ONE, UP)
            True
            >>> Face(ZERO, ONE, UP) + DOWN == Face(DOWN, ONE + DOWN, ZERO)
            True
        """
        if not isinstance(other, V3):
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


## Zero-filled vector, equals to V3(0, 0, 0)
ZERO = V3()
## One-filled vector, equals to V3(1, 1, 1)
ONE = V3(1, 1, 1)
## Forward direction vector, equals to V3(1, 0, 0)
FORWARD = V3(x=1)
## Backward direction vector, equals to V3(-1, 0, 0)
BACKWARD = V3(x=-1)
## Left direction vector, equals to V3(0, 1, 0)
LEFT = V3(y=1)
## Right direction vector, equals to V3(0, -1, 0)
RIGHT = V3(y=-1)
## Up direction vector, equals to V3(0, 0, 1)
UP = V3(z=1)
## Down direction vector, equals to V3(0, 0, -1)
DOWN = V3(z=-1)