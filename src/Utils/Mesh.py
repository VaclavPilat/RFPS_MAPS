## \file
# Classes for representing mesh data
# \todo Refactor and add tests
from . import Decorators, Helpers, Colors, Vector


@Decorators.makeImmutable
@Decorators.addInitRepr
class Line:
    """A line connecting two points.
    """

    def __init__(self, a: Vector.V3, b: Vector.V3) -> None:
        """Initialize a line.

        Args:
            a (Vector.V3): First point of the line.
            b (Vector.V3): Second point of the line.
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
        """Making a copy of a line with altered arguments.

        Returns:
            Line: A copy of the line with altered params.
        """
        # noinspection PyCallingNonCallable
        return Line(self.a(*args, **kwargs), self.b(*args, **kwargs))

    def __iter__(self):
        """Iterating over line bounds
        """
        yield self.a
        yield self.b

    def __add__(self, other: Vector.V3) -> "Line":
        """Incrementing line bounds by a vector

        Args:
            other (Vector.V3): Vector to add

        Returns:
            Line: A copy of the line with offset line bounds.
        """
        return Line(*(point + other for point in self))

    def __rshift__(self, other: float) -> "Line":
        """Rotating a line by a vector

        Args:
            other (float): Angle to rotate by

        Returns:
            Line: A copy of the line with rotated line bounds.
        """
        return Line(*(point >> other for point in self))

    ## \note This method only supports comparisons between lines that are parallel to axis.
    def __contains__(self, line: "Line") -> bool:
        """Checking whether a line is contained by this one.

        Args:
            line (Line): Line to check

        Returns:
            bool: True if the line is contained by this one.
        """
        # Quick comparison in case both lines are equal
        if self == line:
            return True
        for point in line:
            # Checking if the point "belongs" on the line defined by self bounds
            if (self.a - self.b) @ (self.a - point):
                return False
            # Checking if the point is "between" self bounds
            if not 0 <= ((self.b - self.a) ** (point - self.a)) <= ((self.b - self.a) ** (self.b - self.a)):
                return False
        return True


# noinspection PyCallingNonCallable
@Decorators.makeImmutable
@Decorators.addInitRepr
@Decorators.addCopyCall("points")
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

    def __iter__(self):
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

    def __add__(self, other: Vector.V3) -> "Face":
        """Incrementing face bounds by a vector

        Args:
            other (Vector.V3): Vector to increment face bounds by

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


@Decorators.addInitRepr
@Decorators.makeImmutable
class Object(metaclass=Helpers.Repr):
    """Class for containing own mesh and/or other objects
    """

    def __init__(self, name: str = "New object", position: Vector.V3 = Vector.V3.ZERO, rotation: float = 0, *args, **kwargs) -> None:
        """Creating a new object

        Args:
            name (str, optional): Object name. Defaults to "New object".
            position (Vector.V3, optional): Object location. Defaults to V3.ZERO.
            rotation (float, optional): Object rotation in degrees (Z-value only). Defaults to 0.
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

    def __matmul__(self, structure: Vector.V3 | Line | Face) -> Face:
        """Transforming structure positions to be relative to parent

        Args:
            structure (Vector.V3 | Line | Face): 3D structure (relative to self position)

        Returns:
            Vector.V3 | Line | Face: Vertex position (relative to parent's position)
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
        self.faces.add(Face(points, **kwargs))

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