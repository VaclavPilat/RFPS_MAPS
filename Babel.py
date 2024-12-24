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



@reprWrapper
class Circle:
    """Data object for storing information used for generating points in circles
    """

    def __init__(self, radius: int|float = 1, points: int = 8, pivot: V3 = V3.ZERO, start: int|float = 0, end: int|float = 360) -> None:
        """Initializing an Circle instance

        Args:
            radius (int | float, optional): Circle radius, in meters. Defaults to 1.
            points (int, optional): Number of points in circle, should be a power of 2. Defaults to 8.
            pivot (V3, optional): Circle pivot point. Defaults to V3.ZERO.
            start (int | float, optional): Circle angle start, in degrees. Defaults to 0.
            end (int | float, optional): Circle angle end, in degrees. Defaults to 360.
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
    
    def generate(self):
        """Generating points on a circle

        Yields:
            V3: Vertex positions
        """
        for i in range(self.points):
            degrees = 360 * i / self.points
            if not (self.start <= degrees <= self.end):
                continue
            radians = math.radians(degrees)
            sin, cos = (f(radians) for f in (math.sin, math.cos))
            yield self.pivot + V3.FORWARD * sin * self.radius + V3.RIGHT * cos * self.radius



class Column(Object):
    """Cylinder mesh with vertical walls only
    """

    def generate(self, height: int|float, circle: Circle) -> None:
        """Generating a column

        Args:
            height (int | float): Column height.
            circle (Circle): Column radius.
        """
        lower = tuple(circle.generate())
        circle.pivot = V3.UP * 5
        upper = tuple(circle.generate())
        for i, j in [(a-1, a) for a in range(circle.points)]:
            self.face([upper[j], upper[i], lower[i], lower[j]])



class CenterWall(Object):
    """Wall around central staircase
    """

    def generate(self, height: int|float, circle: Circle) -> None:
        # Outer wall
        lower = tuple(circle.generate())
        circle.pivot = V3.UP * 5
        upper = tuple(circle.generate())
        for i, j in [(a, a+1) for a in range(len(lower) - 1)]:
            self.face([upper[j], upper[i], lower[i], lower[j]])



class Center(Object):
    """Central spiral staircase sorrounded by walls
    """

    INNER_RADIUS = 1
    WALL_WIDTH = 0.5

    def generate(self, height: int|float, circle: Circle) -> None:
        """Generating a central column with a spiral staircase inside
        """
        self.load(Column, "Central pillar", height=height, circle=Circle(radius=self.INNER_RADIUS, points=circle.points//2))
        self.load(CenterWall, "Central wall", height=height, circle=circle)



class Babel(Object):
    """Implementation of the Tower of Babel map
    """

    FLOOR_HEIGHT = 5
    CENTRAL_RADIUS = 4
    PILLAR_GAP = 3

    def generate(self) -> None:
        """Generating Babel structure
        """
        self.load(Center, "Central staircase", height=self.FLOOR_HEIGHT, circle=Circle(radius=self.CENTRAL_RADIUS, points=32, start=30, end=-30%360))



if __name__ == "__main__":
    Blender.setup()
    Blender.purge()
    scene = Babel("Tower of Babel")
    print(scene)
    scene.build()