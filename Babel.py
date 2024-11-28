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



class SpiralStaircaseWall(Object):
    """Wall sorrounding a spiral staircase
    """

    def generate(self, height: int|float, outer: int|float, inner: int|float, segments: int) -> None:
        """Generating a circular wall around for a spiral staircase

        Args:
            height (int | float): Floor height
            outer (int | float): Outer radius
            inner (int | float): Inner radius
            segments (int): Segment count
        """
        ENTRANCE_GAP = segments // 8
        # Inner walls
        innerLower = tuple(Points.circle(V3.ZERO, inner, segments))
        innerUpper = tuple(Points.circle(V3.ZERO + height * V3.UP, inner, segments))
        for i, j in [(a-1, a) for a in range(ENTRANCE_GAP // 2 + 2, segments - ENTRANCE_GAP // 2)]:
            self.face([innerUpper[i], innerUpper[j], innerLower[j], innerLower[i]])
        # Outer walls
        outerLower = tuple(Points.circle(V3.ZERO, outer, segments))
        outerUpper = tuple(Points.circle(V3.ZERO + height * V3.UP, outer, segments))
        for i, j in [(a-1, a) for a in range(ENTRANCE_GAP // 2 + 2, segments - ENTRANCE_GAP // 2)]:
            self.face([outerUpper[i], outerUpper[j], outerLower[j], outerLower[i]][::-1])



class CentralStaircase(Object):
    """Central spiral staircase sorrounded by walls
    """

    INNER_RADIUS = 0.5
    WALL_WIDTH = 0.5

    def generate(self, height: int|float, radius: int|float, segments: int) -> None:
        """Generating a central column with a spiral staircase inside

        Args:
            height (int | float): Total height
            radius (int | float): Outer radius of the staircase
            segments (int): Outer segment count
        """
        INNER_SEGMENTS = segments // 2
        self.load(Column, "Central pillar", V3.ZERO, height, self.INNER_RADIUS, INNER_SEGMENTS)
        self.load(SpiralStaircaseWall, "Staircase wall", V3.ZERO, height, radius, radius - self.WALL_WIDTH, segments)



class Babel(Object):
    """Implementation of the Tower of Babel map
    """

    FLOOR_HEIGHT = 5
    CENTRAL_RADIUS = 3
    PILLAR_GAP = 3

    def generate(self) -> None:
        """Generating Babel structure
        """
        self.load(CentralStaircase, "Central staircase", V3.ZERO, self.FLOOR_HEIGHT, self.CENTRAL_RADIUS, 32)
        #for point in Points.circle(V3.ZERO, self.CENTRAL_RADIUS + self.PILLAR_GAP, 12):
        #    self.load(Column, "Atrium pillar", point, 3.5, 0.25, 24)



if __name__ == "__main__":
    Blender.setup()
    Blender.purge()
    scene = Babel("Tower of Babel", V3.ZERO)
    print(scene)
    scene.build()