## \file
# Classes for scene or map generation
from Object import Mesh



class Map:
    """Class for representing a map that contains object meshes.
    """

    def __init__(self) -> None:
        """Generating scene objects
        """
        self.objects = []

    def load(self, mesh: "Mesh", *args, **kwargs) -> None:
        """Creating a mesh instance using class type and its constructor arguments

        Args:
            mesh (Mesh): Mesh type to create
        """
        self.objects.append(mesh(*args, **kwargs))



if __name__ == "__main__":
    import unittest
    class MapTest(unittest.TestCase):
        """Class for testing Map implementation
        """
        pass
    unittest.main()