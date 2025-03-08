## \file
# Classes for creating objects
from Math.Vector import V3
from Utils.Decorators import addInitRepr, makeImmutable, defaultKwargsValues



@addInitRepr
@makeImmutable
## \todo Refactor & add docs
class Object:
    """Class for containing own mesh and/or other objectes
    """

    def __init__(self, name: str = "New object", position: V3 = V3.ZERO, *args, **kwargs) -> None:
        """Creating a new object

        Args:
            name (str, optional): Object name. Defaults to "New object".
            position (V3, optional): Object location. Defaults to V3.ZERO.
        """
        self.name = name
        self.position = position
        self.objects = []
        self.faces = []
        self.generate(*args, **kwargs)
    
    def __iter__(self):
        """Iterating over objectes

        Returns:
            Iterator representing object objects
        """
        yield self
        for obj in self.objects:
            yield from obj
    
    def printHierarchy(self, indent: str = "", itemIndent: str = "") -> None:
        """Printing string representation of object hierarchy

        Args:
            indent (str, optional): Default line indent. Defaults to "".
            itemIndent (str, optional): Default item line indent to be passed deeper. Defaults to "".
        """
        print(indent + repr(self))
        for index, child in enumerate(self.objects):
            if index < len(self.objects) - 1:
                child.printHierarchy(itemIndent + "├──", itemIndent + "│  ")
            else:
                child.printHierarchy(itemIndent + "└──", itemIndent + "   ")

    def load(self, obj: "Object", *args, **kwargs) -> "Object":
        """Creating a object instance using class type and its constructor arguments

        Args:
            obj (Object): Object type to create

        Returns:
            Object: Created object instance
        """
        instance = obj(*args, **kwargs)
        self.objects.append(instance)
        return instance
    
    def generate(self) -> None:
        """Generating the object

        Raises:
            NotImplementedError: Thrown when not overriden
        """
        raise NotImplementedError("Object generation method was not overriden")

    def face(self, *vertices, inverted: bool = False) -> None:
        """Creating a new face

        Args:
            inverted (bool, optional): Should the face be inverted? Defaults to False.
        """
        self.faces.append(vertices if not inverted else vertices[::-1])



def createObjectSubclass(cls: "cls" = Object) -> "func":
    """Decorator for creating an Object subclass from a generator function

    Args:
        cls (cls, optional): Object or its subclass type. Defaults to Object.

    Returns:
        cls: Decorator for making a subclass of the provided class type
    """
    def decorator(func: "func") -> "cls":
        class Wrapped(cls):
            pass
        Wrapped.generate = func
        Wrapped.__name__ = func.__name__
        return Wrapped
    return decorator