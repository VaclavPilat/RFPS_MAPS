## \file
# Implementation of the Babel map
if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from Utils.Vector import V3
from Utils.Object import Object
from Utils.Blender import Blender
import math



class Column(Object):
    """Cylinder mesh with vertical walls only
    """

    def points(self, pivot: V3, radius: int|float, segments: int) -> list[V3]:
        """Generating a list of points around a circle

        Args:
            pivot (V3): Center point
            radius (int | float): Circle radius
            segments (int): Segment (point) count

        Returns:
            list[V3]: List of vertex positions
        """
        points = []
        for i in range(segments):
            degrees = 360*i/segments
            sin = math.sin(math.radians(degrees)) * radius
            cos = math.cos(math.radians(degrees)) * radius
            points.append(pivot + V3.FORWARD * sin + V3.RIGHT * cos)
        return points

    def generate(self, height: int|float, radius: int|float, segments: int) -> None:
        """Generating a column

        Args:
            height (int | float): Column height.
            radius (int | float): Column radius.
            segments (int): Number of outer vertical faces.
        """
        lower = self.points(self.pivot, radius, segments)
        upper = self.points(self.pivot + V3.UP * height, radius, segments)



class Babel(Object):
    """Implementation of the Tower of Babel map
    """

    def generate(self) -> None:
        """Generating Babel structure
        """
        self.load(Column, "Central column", V3.ZERO, 5, 0.5, 8)



if __name__ == "__main__":
    Blender.setup()
    Blender.purge()
    scene = Babel("Tower of Babel", V3.ZERO)
    print(scene)
    scene.create()