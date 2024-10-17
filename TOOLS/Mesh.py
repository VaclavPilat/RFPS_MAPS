## \file
# Classes for creating objects and meshes
from Vector import V3



class Mesh:
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
        self.generate(*args, **kwargs)
    
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
    unittest.main()