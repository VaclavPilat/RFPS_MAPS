## \file
# Classes for creating objects and meshes
from Vector import V3



class Container:
    """Class for containing a list of meshes
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initializing the container and generating its structure
        """
        self.objects = []
        self.generate(*args, **kwargs)
    
    def __iter__(self):
        """Iterating over meshes

        Returns:
            Iterator representing mesh objects
        """
        yield self
        for obj in self.objects:
            yield from obj

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



class Mesh(Container):
    """Class for representing the mesh of an object as a collection of faces
    """

    def __init__(self, name: str = "New mesh", pivot: V3 = V3.ZERO, *args, **kwargs) -> None:
        """Creating a new mesh

        Args:
            name (str, optional): Mesh name. Defaults to "New mesh".
            pivot (V3, optional): Pivot positions. Defaults to V3.ZERO.
        """
        self.name = name
        self.pivot = pivot
        self.faces = []
        super().__init__(*args, **kwargs)

    def face(self, vertices: list[V3]|tuple[V3], material: int = 0) -> None:
        """Creating a new face

        Args:
            vertices (list[V3] | tuple[V3]): List of bounding vertex positions
            material (int, optional): Material index. Defaults to 0.
        """
        self.faces.append(vertices)



if __name__ == "__main__":
    import unittest
    class MeshTest(unittest.TestCase):
        """Class for testing Mesh implementation
        """
        def test_constructor(self) -> None:
            """Testing that basic constructor works
            """
            with self.assertRaises(NotImplementedError):
                Mesh()
        def test_overwriting(self) -> None:
            """Overwriting the generate() method on Mesh
            """
            class OverwrittenMesh(Mesh):
                def generate(self, value: int) -> None:
                    self.value = value
            self.assertEqual(OverwrittenMesh(value=10).value, 10)
        def test_nesting(self) -> None:
            """Counting the nested meshes in a container
            """
            class AMesh(Mesh):
                def generate(self) -> None:
                    pass
            class BMesh(Mesh):
                def generate(self) -> None:
                    self.load(AMesh)
            class CMesh(Mesh):
                def generate(self, inner: "Mesh") -> None:
                    self.load(inner)
            a = AMesh()
            self.assertEqual(len(list(a)), 1)
            a.load(AMesh)
            self.assertEqual(len(list(a)), 2)
            a.load(BMesh)
            self.assertEqual(len(list(a)), 4)
            a.load(CMesh, inner=AMesh)
            self.assertEqual(len(list(a)), 6)
            a.load(CMesh, inner=BMesh)
            self.assertEqual(len(list(a)), 9)
    unittest.main()