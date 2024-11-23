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



class Points:
    """Math functions for generating points
    """

    @staticmethod
    def circle(pivot: V3, radius: int|float, count: int):
        """Generating a list of points around a circle

        Args:
            pivot (V3): Center point
            radius (int | float): Circle radius
            count (int): Segment (point) count

        Yields:
            V3: Vertex position
        """
        for i in range(count):
            degrees = math.radians(360 * i / count)
            sin = math.sin(degrees) * radius
            cos = math.cos(degrees) * radius
            yield pivot + V3.FORWARD * sin + V3.RIGHT * cos



class Column(Object):
    """Cylinder mesh with vertical walls only
    """

    def generate(self, height: int|float, radius: int|float, segments: int) -> None:
        """Generating a column

        Args:
            height (int | float): Column height.
            radius (int | float): Column radius.
            segments (int): Number of outer vertical faces.
        """
        lower = tuple(Points.circle(self.pivot, radius, segments))
        upper = tuple(Points.circle(self.pivot + V3.UP * height, radius, segments))
        for i, j in [(a-1, a) for a in range(segments)]:
            self.face([upper[j], upper[i], lower[i], lower[j]])



class Babel(Object):
    """Implementation of the Tower of Babel map
    """

    def generate(self) -> None:
        """Generating Babel structure
        """
        self.load(Column, "Central column", V3.ZERO, 5, 2.5, 64)
        for point in Points.circle(V3.ZERO, 5, 10):
            self.load(Column, "Atrium pillar", point, 5, 0.3, 24)



if __name__ == "__main__":
    Blender.setup()
    Blender.purge()
    scene = Babel("Tower of Babel", V3.ZERO)
    print(scene)
    scene.build()