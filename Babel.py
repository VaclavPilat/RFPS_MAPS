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
from Utils.Wrapper import reprWrapper
import math



class Math:
    """General math functions
    """

    @staticmethod
    def isPow2(number: int) -> bool:
        """Checking whether a number is a power of 2

        Args:
            number (int): Number to check

        Returns:
            bool: True if the number is a non-zero power of 2
        """
        return number > 0 and (number & (number - 1)) == 0



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



@reprWrapper
class Arc:
    """Data object for storing information used for generating real arcs and circles
    """

    def __init__(self, radius: int|float = 1, points: int = 8, pivot: V3 = V3.ZERO, start: int|float = 0, end: int|float = 360) -> None:
        """Initializing an Arc instance

        Args:
            radius (int | float, optional): Arc radius, in meters. Defaults to 1.
            points (int, optional): Number of points in arc, should be a power of 2. Defaults to 8.
            start (int | float, optional): Arc angle start, in degrees. Defaults to 0.
            end (int | float, optional): Arc angle end, in degrees. Defaults to 360.
        """
        assert radius > 0, "Radius has to be a positive number"
        self.radius = radius
        assert Math.isPow2(points), "Point count has to be a power of 2"
        self.points = points
        self.pivot = pivot
        assert start >= 0, "Start has to be greater than or equal to 0"
        self.start = start
        assert end <= 360, "End has to lesser than or equal to 360"
        self.end = end



class Column(Object):
    """Cylinder mesh with vertical walls only
    """

    def generate(self, height: int|float, arc: Arc) -> None:
        """Generating a column

        Args:
            height (int | float): Column height.
            arc (Arc): Column radius.
        """
        lower = tuple(Points.circle(arc.pivot, arc.radius, arc.points))
        upper = tuple(Points.circle(arc.pivot + V3.UP * height, arc.radius, arc.points))
        for i, j in [(a-1, a) for a in range(arc.points)]:
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

    def generate(self, height: int|float, arc: Arc) -> None:
        """Generating a central column with a spiral staircase inside

        Args:
            height (int | float): Total height
            radius (int | float): Outer radius of the staircase
            segments (int): Outer segment count
        """
        INNER_SEGMENTS = arc.points // 2
        self.load(Column, "Central pillar", V3.ZERO, height, Arc(self.INNER_RADIUS, INNER_SEGMENTS))
        self.load(SpiralStaircaseWall, "Staircase wall", V3.ZERO, height, arc.radius, arc.radius - self.WALL_WIDTH, arc.points)



class Babel(Object):
    """Implementation of the Tower of Babel map
    """

    FLOOR_HEIGHT = 5
    CENTRAL_RADIUS = 3
    PILLAR_GAP = 3

    def generate(self) -> None:
        """Generating Babel structure
        """
        self.load(CentralStaircase, "Central staircase", V3.ZERO, self.FLOOR_HEIGHT, Arc(radius=self.FLOOR_HEIGHT, points=32))
        #for point in Points.circle(V3.ZERO, self.CENTRAL_RADIUS + self.PILLAR_GAP, 12):
        #    self.load(Column, "Atrium pillar", point, 3.5, 0.25, 24)



if __name__ == "__main__":
    Blender.setup()
    Blender.purge()
    scene = Babel("Tower of Babel", V3.ZERO)
    print(scene)
    scene.build()