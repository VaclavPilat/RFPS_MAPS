"""! \file
Classes for representing a model.
"""
from .Decorators import addInitRepr, makeImmutable
from .Mesh import Vector, Line, Face, ZERO
from .Colors import Hierarchy
from .Helpers import Repr


@addInitRepr
@makeImmutable
class Object(metaclass=Repr):
    """Class for containing own mesh and/or other Object instances.

    This class is meant to be a base class, as shown the exception being thrown in Object.__call__.
    """

    def __init__(self, name: str = "New object", position: Vector = ZERO, rotation: int = 0, *args, **kwargs) -> None:
        """Creating a new object

        Args:
            name (str, optional): Object name. Defaults to "New object".
            position (Vector, optional): Object location. Defaults to ZERO.
            rotation (int, optional): Object rotation in degrees (Z-value only). Defaults to 0.
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
        # Generating mesh
        self(*args, **kwargs)

    def __call__(self, *args, **kwargs) -> None:
        """Generating the model mesh.

        Gets automatically called from the constructor.

        Raises:
            NotImplementedError: Thrown when not overridden

        Examples:
            >>> Object()
            Traceback (most recent call last):
            NotImplementedError: Object generation method was not overwritten
        """
        raise NotImplementedError("Object generation method was not overwritten")

    def __iter__(self):
        """Iterating over objects

        Returns:
            Iterator representing object objects
        """
        yield self
        for obj in self.objects:
            yield from obj

    def __matmul__(self, structure: Vector | Line | Face) -> Face:
        """Transforming structure positions to be relative to parent

        Args:
            structure (Vector | Line | Face): 3D structure (relative to self position)

        Returns:
            Vector | Line | Face: Vertex position (relative to parent's position)
        """
        return (structure >> self.rotation) + self.position

    def __iadd__(self, other) -> "Object":
        """Adding another Object or Face to self

        Args:
            other (Object | Face): Face or Object instance to add

        Returns:
            Object: Self reference
        """
        if isinstance(other, Object):
            self.objects.append(other)
        elif isinstance(other, Face):
            self.faces.add(other)
        else:
            raise TypeError(f"Unexpected argument type: {type(other)}")
        return self

    def __str__(self, current: str = "", children: str = "", layer: int = 0) -> None:
        """Getting the string representation of object hierarchy

        Args:
            current (str, optional): Current line indent. Defaults to "".
            children (str, optional): Line indent for child items. Defaults to "".
            layer (int, optional): Current layer index. Defaults to 0.
        """
        output = f"{current}{repr(self)}"
        for index, child in enumerate(self.objects):
            last = index < len(self.objects) - 1
            output += "\n" + child.__str__(
                f"{children}{Hierarchy(layer)(('┣' if last else '┗') + '━━ ')}",
                f"{children}{Hierarchy(layer)(('┃' if last else ' ') + '   ')}",
                layer + 1
            )
        return output


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

        Wrapped.__call__ = func
        Wrapped.__name__ = func.__name__
        return Wrapped

    return decorator