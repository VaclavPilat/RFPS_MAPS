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
        assert 0 <= start <= 360, "Start has to be between 0 and 360"
        assert start < end, "Start has to be lesser than end"
        self.start = start
        assert 0 <= end <= 360, "End has to between 0 and 360"
        self.end = end
    
    def generate(self) -> tuple:
        """Generating points on a circle

        Returns:
            tuple: Tuple of generated point positions
        """
        points = [360 * i / self.points for i in range(self.points)]
        degrees = [p for p in points if self.start < p < self.end]
        if self.start not in degrees:
            degrees.insert(0, self.start)
        if self.end % 360 not in degrees:
            degrees.append(self.end)
        radians = [math.radians(d) for d in degrees]
        return tuple(self.pivot + (V3.FORWARD * math.sin(r) + V3.RIGHT * math.cos(r)) * self.radius for r in radians)



class Column(Object):
    """Cylinder mesh with vertical walls only
    """

    def generate(self, height: int|float, circle: Circle) -> None:
        """Generating a column

        Args:
            height (int | float): Column height.
            circle (Circle): Column radius.
        """
        lower = circle.generate()
        circle.pivot = V3.UP * height
        upper = circle.generate()
        for i, j in [(a-1, a) for a in range(circle.points)]:
            self.face([upper[j], upper[i], lower[i], lower[j]])



class CenterWall(Object):
    """Wall around central staircase
    """

    def generate(self, height: int|float, circle: Circle) -> None:
        # Outer wall
        outer_lower = circle.generate()
        circle.pivot = V3.UP * height
        outer_upper = circle.generate()
        for i, j in [(a, a+1) for a in range(len(outer_lower) - 1)]:
            self.face([outer_upper[j], outer_upper[i], outer_lower[i], outer_lower[j]])
        # Inner wall
        circle.pivot = V3.ZERO
        circle.radius -= 0.5
        inner_lower = circle.generate()
        circle.pivot = V3.UP * height
        inner_upper = circle.generate()
        for i, j in [(a, a+1) for a in range(len(inner_lower) - 1)]:
            self.face([inner_upper[i], inner_upper[j], inner_lower[j], inner_lower[i]])
        # Walls between outer and inner
        self.face([outer_upper[0], inner_upper[0], inner_lower[0], outer_lower[0]])
        self.face([inner_upper[-1], outer_upper[-1], outer_lower[-1], inner_lower[-1]])



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