## \file
# Classes for creating objects and meshes
try:
    from Vector import V3
except:
    from Utils.Vector import V3
import bpy, bmesh



class Object:
    """Class for containing other meshes
    """

    def __init__(self, name: str = "New object", pivot: V3 = V3.ZERO, *args, **kwargs) -> None:
        """Creating a new mesh

        Args:
            name (str, optional): Mesh name. Defaults to "New mesh".
            pivot (V3, optional): Pivot positions. Defaults to V3.ZERO.
        """
        self.name = name
        self.pivot = pivot
        self.objects = []
        self.faces = []
        self.argstring = ", ".join([repr(a) for a in (name, pivot) + args] + [f"{k}={repr(kwargs[k])}" for k in kwargs])
        self.generate(*args, **kwargs)
    
    def __iter__(self):
        """Iterating over meshes

        Returns:
            Iterator representing mesh objects
        """
        yield self
        for obj in self.objects:
            yield from obj
    
    def __repr__(self) -> str:
        """Getting the representation of a Mesh instance

        Returns:
            str: String representation of a constructor call with parameters
        """
        return f"{self.__class__.__name__}({self.argstring})"

    def stringify(self, obj: "Object", indent: str = "", itemIndent: str = "") -> str:
        """Getting the string representation of object hierearchy

        Args:
            obj (Object): Object to return string representation of
            indent (str, optional): Default line indent. Defaults to "".
            itemIndent (str, optional): Default item line indent to be passed deeper. Defaults to "".

        Returns:
            str: Hierarchical representation of an object
        """
        output = indent + repr(obj) + "\n"
        for index, child in enumerate(obj.objects):
            if index < len(obj.objects) - 1:
                output += self.stringify(child, itemIndent + "├──", itemIndent + "│  ")
            else:
                output += self.stringify(child, itemIndent + "└──", itemIndent + "   ")
        return output
    
    def __str__(self) -> str:
        """Getting object hierarchy

        Returns:
            str: String representation of object hierarchy
        """
        return self.stringify(self)

    def load(self, mesh: "Mesh", *args, **kwargs) -> None:
        """Creating a mesh instance using class type and its constructor arguments

        Args:
            mesh (Mesh): Mesh type to create
        """
        self.objects.append(mesh(*args, **kwargs))
    
    def generate(self) -> None:
        """Generating the mesh

        Raises:
            NotImplementedError: Thrown when not overriden
        """
        raise NotImplementedError("Mesh generation method was not overriden")

    def face(self, vertices: list[V3]|tuple[V3], material: int = 0) -> None:
        """Creating a new face

        Args:
            vertices (list[V3] | tuple[V3]): List of bounding vertex positions
            material (int, optional): Material index. Defaults to 0.
        """
        self.faces.append(vertices)
    
    def create(self) -> "bpy object":
        """Creating a blender object from an Object instance

        Returns:
            bpy object: Created blender object
        """
        if len(self.faces):
            obj = bpy.data.objects.new(self.name, bpy.data.meshes.new(self.name))
        else:
            obj = bpy.data.objects.new(self.name, None)
        bpy.context.scene.collection.objects.link(obj)
        for child in self.objects:
            child.create().parent = obj
        return obj