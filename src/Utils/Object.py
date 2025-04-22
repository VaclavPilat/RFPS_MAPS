## \file
# Classes for creating objects
from .Line import Line
from .Vector import V3
from .Decorators import addInitRepr, makeImmutable
from .Colors import HIERARCHY, NONE
from .Grid import Grid
from .Face import Face
from types import FunctionType
from typing import Callable


class Repr(type):
    """Custom type for having a __repr__ method that returns type name
    """

    def __repr__(cls) -> str:
        """Returns name of current type

        Returns:
            str: Name of the current type
        """
        return cls.__name__


@addInitRepr
@makeImmutable
## \todo Refactor & add docs
class Object(metaclass=Repr):
    """Class for containing own mesh and/or other objects
    """

    def __init__(self, name: str = "New object", position: V3 = V3.ZERO, rotation: float = 0, *args, **kwargs) -> None:
        """Creating a new object

        Args:
            name (str, optional): Object name. Defaults to "New object".
            position (V3, optional): Object location. Defaults to V3.ZERO.
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

    def transform(self, structure: V3 | Line | Face) -> V3:
        """Getting the position of a point relative to parent

        Args:
            structure (V3 | Line | Face): 3D structure (relative to object position)

        Returns:
            V3 | Line | Face: Vertex position (relative to parent's object position)
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
        print(f"{current}{NONE}{repr(self)}")
        for index, child in enumerate(self.objects):
            color = HIERARCHY[layer % len(HIERARCHY)]
            last = index < len(self.objects) - 1
            newCurrent = f"{children}{color}{'┣' if last else '┗'}━━ "
            newChildren = f"{children}{color}{'┃' if last else ' '}   "
            child.printHierarchy(newCurrent, newChildren, layer + 1)

    def printGrids(self, *args, **kwargs) -> None:
        """Printing out grids representing the current object
        """
        Grid(self).print(*args, **kwargs)


def createObjectSubclass(cls: type = Object) -> Callable[[FunctionType], type]:
    """Decorator for creating an Object subclass from a generator function

    Args:
        cls (type, optional): Object or its subclass type. Defaults to Object.

    Returns:
        type: Decorator for making a subclass of the provided class type
    """

    def decorator(func: FunctionType) -> type:
        class Wrapped(cls):
            pass

        Wrapped.generate = func
        Wrapped.__name__ = func.__name__
        return Wrapped

    return decorator