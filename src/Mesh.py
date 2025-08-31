"""! \file
Classes for representing mesh structure.

Mesh data is stored in Object instances (a recursive tree-like structures).
Each Object may contain multiple Face objects which are represented by Line objects.

\internal
Examples:
"""
from .Vector import V3
from .Decorators import makeImmutable, addOperators, addInitRepr
from . import Helpers, Colors


@addOperators
@makeImmutable
@addInitRepr
class Line:
    """A line between two points.

    It is defined as a set of 2 vertices (since it does not have a direction).

    Examples:
        >>> Line(V3.ZERO, V3.ZERO)
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
            >>> Line(V3.ZERO, V3.ONE) == Line(V3.ZERO, V3.ONE)
            True
            >>> Line(V3.ZERO, V3.ONE) == Line(V3.ONE, V3.ZERO)
            True
            >>> Line(V3.ZERO, V3.ONE) == Line(V3.ONE, V3.LEFT)
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
            >>> hash(Line(V3.ZERO, V3.ONE)) == hash(Line(V3.ONE, V3.ZERO))
            True
            >>> hash(Line(V3.ZERO, V3.ONE)) == hash(Line(V3.ONE, V3.LEFT))
            False
        """
        return hash(frozenset((self.a, self.b)))

    def __call__(self, *args, **kwargs) -> "Line":
        """Making a copy of a line with altered arguments.

        Returns:
            Line: A copy of the line with altered params.

        Examples:
            >>> Line(V3.LEFT, V3.RIGHT)() == Line(V3.LEFT, V3.RIGHT)
            True
            >>> Line(V3.ONE, V3.UP)(z=0) == Line(V3(x=1, y=1, z=0), V3(x=0, y=0, z=0))
            True
        """
        # noinspection PyCallingNonCallable
        return Line(self.a(*args, **kwargs), self.b(*args, **kwargs))

    def __iter__(self):
        """Iterating over line bounds

        Examples:
            >>> list(Line(V3.LEFT, V3.RIGHT)) == [V3.LEFT, V3.RIGHT]
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
            >>> Line(V3.ONE, V3.UP) + V3.UP == Line(V3(1, 1, 2), V3(0, 0, 2))
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
            >>> Line(V3.FORWARD, V3.LEFT) >> 90 == Line(V3.RIGHT, V3.FORWARD)
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
            >>> Line(V3.ZERO, V3.ONE) | Line(V3.ZERO, V3.ONE)
            True
            >>> Line(V3.ZERO, V3.ONE) | Line(V3.UP, V3.ONE + V3.UP)
            True
            >>> Line(V3.ZERO, V3.ONE) | Line(V3.UP, V3.RIGHT)
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
        >>> Face(V3.ZERO, V3.RIGHT)
        Traceback (most recent call last):
        ValueError: Face must have at least 3 vertices
        >>> Face(V3.ZERO, V3.LEFT, V3.ZERO)
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
            >>> tuple(Face(V3.ZERO, V3.ONE, V3.UP)) == (Line(V3.UP, V3.ZERO), Line(V3.ZERO, V3.ONE), Line(V3.ONE, V3.UP))
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
            >>> Face(V3.ZERO, V3.ONE, V3.UP) == Face(V3.ZERO, V3.ONE, V3.UP)
            True
            >>> Face(V3.ZERO, V3.ONE, V3.UP) == Face(V3.ONE, V3.UP, V3.ZERO)
            True
            >>> Face(V3.ZERO, V3.ONE, V3.UP) == Face(V3.ZERO, V3.UP, V3.ONE)
            False
            >>> Face(V3.ZERO, V3.UP, V3.ONE) == Face(V3.ZERO, V3.UP, V3.DOWN)
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
            >>> hash(Face(V3.ZERO, V3.ONE, V3.UP)) == hash(Face(V3.ZERO, V3.ONE, V3.UP))
            True
            >>> hash(Face(V3.ZERO, V3.ONE, V3.UP)) == hash(Face(V3.ONE, V3.UP, V3.ZERO))
            True
            >>> hash(Face(V3.ZERO, V3.ONE, V3.UP)) == hash(Face(V3.ZERO, V3.UP, V3.ONE))
            False
            >>> hash(Face(V3.ZERO, V3.UP, V3.ONE)) == hash(Face(V3.ZERO, V3.UP, V3.DOWN))
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
            >>> Face(V3.ZERO, V3.ONE, V3.UP) + V3.ZERO == Face(V3.ZERO, V3.ONE, V3.UP)
            True
            >>> Face(V3.ZERO, V3.ONE, V3.UP) + V3.DOWN == Face(V3.DOWN, V3.ONE + V3.DOWN, V3.ZERO)
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
            >>> Face(V3.ZERO, V3.ONE, V3.UP) >> 0 == Face(V3.ZERO, V3.ONE, V3.UP)
            True
            >>> Face(V3.ZERO, V3.FORWARD, V3.RIGHT) >> 90 == Face(V3.ZERO, V3.RIGHT, V3.BACKWARD)
            True
        """
        return Face(*(point >> other for point in self.points))


@addInitRepr
@makeImmutable
class Object(metaclass=Helpers.Repr):
    """Class for containing own mesh and/or other objects
    """

    def __init__(self, name: str = "New object", position: V3 = V3.ZERO, rotation: int|float = 0, *args, **kwargs) -> None:
        """Creating a new object

        Args:
            name (str, optional): Object name. Defaults to "New object".
            position (V3, optional): Object location. Defaults to V3.ZERO.
            rotation (int | float, optional): Object rotation in degrees (Z-value only). Defaults to 0.
        """
        ## Object name
        self.name = name
        ## Object location
        self.position = position
        ## Object rotation (in degrees)
        self.rotation = rotation
        ## List of child objects
        self.objects = []
        ## List of mesh faces
        self.faces = set()
        # noinspection PyArgumentList
        self.generate(*args, **kwargs)

    def __iter__(self):
        """Iterating over objects

        Returns:
            Iterator representing object objects
        """
        yield self
        for obj in self.objects:
            yield from obj

    def __matmul__(self, structure: V3 | Line | Face) -> Face:
        """Transforming structure positions to be relative to parent

        Args:
            structure (V3 | Line | Face): 3D structure (relative to self position)

        Returns:
            V3 | Line | Face: Vertex position (relative to parent's position)
        """
        return (structure >> self.rotation) + self.position

    def load(self, obj: type, *args, **kwargs) -> "Object":
        """Creating an object instance using Object type and its constructor arguments

        Args:
            obj (type): Object type to create

        Returns:
            Object: Created object instance
        """
        instance = obj(*args, **kwargs)
        self.objects.append(instance)
        return instance

    def generate(self) -> None:
        """Generating the object

        Raises:
            NotImplementedError: Thrown when not overridden
        """
        raise NotImplementedError("Object generation method was not overridden")

    def face(self, *points, **kwargs) -> None:
        """Creating a new face
        """
        self.faces.add(Face(*points, **kwargs))

    def printHierarchy(self, current: str = "", children: str = "", layer: int = 0) -> None:
        """Printing string representation of object hierarchy

        Args:
            current (str, optional): Current line indent. Defaults to "".
            children (str, optional): Line indent for child items. Defaults to "".
            layer (int, optional): Current layer index. Defaults to 0.
        """
        print(f"{current}{Colors.NONE}{repr(self)}")
        for index, child in enumerate(self.objects):
            color = Colors.HIERARCHY[layer % len(Colors.HIERARCHY)]
            last = index < len(self.objects) - 1
            newCurrent = f"{children}{color}{'┣' if last else '┗'}━━ "
            newChildren = f"{children}{color}{'┃' if last else ' '}   "
            child.printHierarchy(newCurrent, newChildren, layer + 1)


def createObjectSubclass(cls: type = Object):
    """Decorator for creating an Object subclass from a generator function

    Args:
        cls (type, optional): Object or its subclass type. Defaults to Object.

    Returns:
        Decorator for making a subclass of the provided class type
    """

    def decorator(func) -> type:
        class Wrapped(cls):
            pass

        Wrapped.generate = func
        Wrapped.__name__ = func.__name__
        return Wrapped

    return decorator