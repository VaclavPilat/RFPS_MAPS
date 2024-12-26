## \file
# Classes for creating objects
from Utils.Vector import V3
from Utils.Wrapper import reprWrapper
import bpy, bmesh



@reprWrapper
class Object:
    """Class for containing own mesh and/or other objectes
    """

    def __init__(self, name: str = "New object", pivot: V3 = V3.ZERO, *args, **kwargs) -> None:
        """Creating a new object

        Args:
            name (str, optional): Object name. Defaults to "New object".
            pivot (V3, optional): Pivot positions. Defaults to V3.ZERO.
        """
        self.name = name
        self.pivot = pivot
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
    
    def __str__(self, indent: str = "", itemIndent: str = "") -> str:
        """Getting the string representation of object hierearchy

        Args:
            indent (str, optional): Default line indent. Defaults to "".
            itemIndent (str, optional): Default item line indent to be passed deeper. Defaults to "".

        Returns:
            str: Hierarchical representation of an object
        """
        output = indent + repr(self) + "\n"
        for index, child in enumerate(self.objects):
            if index < len(self.objects) - 1:
                output += child.__str__(itemIndent + "├──", itemIndent + "│  ")
            else:
                output += child.__str__(itemIndent + "└──", itemIndent + "   ")
        return output
    
    def print(self) -> "Object":
        """Printing object structure

        Returns:
            Object: Self reference
        """
        print(self)
        return self

    def load(self, obj: "Object", *args, **kwargs) -> None:
        """Creating a object instance using class type and its constructor arguments

        Args:
            obj (Object): Object type to create
        """
        self.objects.append(obj(*args, **kwargs))
    
    def generate(self) -> None:
        """Generating the object

        Raises:
            NotImplementedError: Thrown when not overriden
        """
        raise NotImplementedError("Object generation method was not overriden")

    def face(self, vertices: list[V3]|tuple[V3], inverted: bool = False) -> None:
        """Creating a new face

        Args:
            vertices (list[V3] | tuple[V3]): List of bounding vertex positions
            inverted (bool, optional): Should the face be inverted? Defaults to False.
        """
        self.faces.append(vertices if not inverted else vertices[::-1])
    
    def create(self) -> "bpy mesh":
        """Creating a blender mesh from face vertices

        Returns:
            bpy mesh: Created mesh object
        """
        mesh = bpy.data.meshes.new(self.name)
        bm = bmesh.new()
        vertices = {}
        for face in self.faces:
            for vert in face:
                if vert not in vertices:
                    vertices[vert] = bm.verts.new(tuple(vert))
            bm.faces.new([vertices[vert] for vert in face])
        bm.to_mesh(mesh)
        return mesh
    
    def build(self) -> "bpy object":
        """Building a blender object from an Object instance

        Returns:
            bpy object: Built blender object
        """
        obj = bpy.data.objects.new(self.name, self.create() if len(self.faces) else None)
        obj.location = list(self.pivot)
        bpy.context.scene.collection.objects.link(obj)
        for child in self.objects:
            child.build().parent = obj
        return obj