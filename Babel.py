## \file
# Implementation of the Babel map
from Utils.Scene import Scene
from Utils.Mesh import Mesh
from Utils.Vector import V3



class Column(Mesh):
    """Cylinder mesh with vertical walls only
    """

    def generate(self, height: int|float = 5, radius: int|float = 0.5, segments: int = 8) -> None:
        """Generating a column

        Args:
            height (int | float, optional): Column height. Defaults to 5.
            radius (int | float, optional): Column radius. Defaults to 0.5.
            segments (int, optional): Number of outer vertical faces. Defaults to 8.
        """
        pass



class Babel(Scene):
    """Implementation of the Tower of Babel map
    """

    def generate(self) -> None:
        """Generating Babel structure
        """
        pass



if __name__ == "__main__":
    Babel().create()