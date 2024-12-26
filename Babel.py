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

    def __init__(self, radius: int|float = 1, points: int = 8, pivot: V3 = V3.ZERO, bounds: tuple = None) -> None:
        """Initializing an Circle instance

        Args:
            radius (int | float, optional): Circle radius, in meters. Defaults to 1.
            points (int, optional): Number of points in circle, should be a power of 2. Defaults to 8.
            pivot (V3, optional): Circle pivot point. Defaults to V3.ZERO.
            bounds (tuple, optional): Pair of angle bound values in degrees. Defaults to None.
        """
        assert radius > 0, "Radius has to be a positive number"
        self.radius = radius
        assert Math.isPow2(points), "Point count has to be a power of 2"
        self.points = points
        self.pivot = pivot
        if bounds is not None:
            assert 0 <= bounds[0] < bounds[1] <= 360, "Both bounds have to between 0 and 360 and the first one has to be lesser than the seconds one"
        self.bounds = bounds
    
    def vertices(self) -> tuple:
        """Generating vertex points on a circle

        Returns:
            tuple: Tuple of generated vertex positions
        """
        ## \todo Change start/end generation so that both of these points are the lines which were cut off rather than on the circle itself
        degrees = [360 * i / self.points for i in range(self.points)]
        if self.bounds is not None:
            degrees = [d for d in degrees if self.bounds[0] <= d <= self.bounds[1]]
            ## \todo Find a better solution instead of this if statement
            if self.bounds[1] == 360:
                degrees.append(360)
        radians = [math.radians(d) for d in degrees]
        return tuple(self.pivot + (V3.FORWARD * math.sin(r) + V3.RIGHT * math.cos(r)) * self.radius for r in radians)
    
    def cylinder(self, height: int|float, inverted: bool = False, closed: bool = True):
        """Generating cylinder walls

        Args:
            height (int | float): Cylinder height
            inverted (bool, optional): Should the faces be inverted? Defaults to False.
            closed (bool, optional): Should the cylinder be closed? Defaults to True.

        Yields:
            tuple: Sequences of vertices for each face
        """
        lower = self.vertices()
        upper = self(pivot=self.pivot + V3.UP * height).vertices()
        for i, j in [(a-1, a) for a in range(not closed, len(lower))]:
            yield (upper[i], upper[j], lower[j], lower[i]) if inverted else (upper[j], upper[i], lower[i], lower[j])
    
    def face(self, cutout: "Circle" = None) -> tuple:
        """Generating circle face

        Args:
            cutout (Circle, optional): Circular hole dimensions. Defaults to None.

        Returns:
            tuple: Sequence of vertices
        """
        if cutout is None:
            return self.vertices()
        assert cutout.radius < self.radius, "A hole has to be smaller that the object it is a part of!"
        return self.vertices() + cutout.vertices()[::-1]
    
    def __call__(self, **kwargs) -> "Circle":
        """Creating a new Circle instance by modifying current fields

        Returns:
            Circle: New Circle instance
        """
        data = {
            "radius": self.radius,
            "points": self.points,
            "pivot": self.pivot,
            "bounds": self.bounds
        }
        data.update(**kwargs)
        return Circle(**data)



class Column(Object):
    """Cylinder mesh with vertical walls only
    """

    def generate(self, height: int|float, circle: Circle) -> None:
        """Generating a column

        Args:
            height (int | float): Column height.
            circle (Circle): Column radius.
        """
        assert circle.bounds is None, "Column cannot have overwritten circle angle bounds"
        for face in circle.cylinder(height):
            self.face(face)



class CenterWall(Object):
    """Wall around central staircase
    """

    def generate(self, height: int|float, outer: Circle, inner: Circle) -> None:
        """Generating walls around spiral

        Args:
            height (int | float): Object height
            outer (Circle): Outer wall circle
            inner (Circle): Inner wall circle
        """
        # Outer wall
        for face in outer.cylinder(height, closed=False):
            self.face(face)
        # Inner wall
        for face in inner.cylinder(height, inverted=True, closed=False):
            self.face(face)
        # Walls between outer and inner
        #self.face([outer_upper[0], inner_upper[0], inner_lower[0], outer_lower[0]])
        #self.face([inner_upper[-1], outer_upper[-1], outer_lower[-1], inner_lower[-1]])



class Center(Object):
    """Central spiral staircase sorrounded by walls
    """

    def generate(self, height: int|float, outer: Circle) -> None:
        """Generating a central column with a spiral staircase inside

        Args:
            height (int | float): Object height
            outer (Circle): Outer circle
        """
        inner = outer(radius=outer.radius - 0.5)
        column = Circle(radius=1, points=outer.points//2)
        self.load(Column, "Central pillar", height=height, circle=column)
        self.load(CenterWall, "Central wall", height=height, outer=outer, inner=inner)



class AtriumFloor(Object):
    """Floor of the atrium
    """

    def generate(self, height: int|float, outer: Circle, inner: Circle) -> None:
        """Generating atrium floor

        Args:
            height (int | float): Floor height
            outer (Circle): Outer circle
            inner (Circle): Inner circle
        """
        self.face(outer.face(cutout=inner))



class Atrium(Object):
    """Atrium in the center of the map
    """

    def generate(self, height: int|float, outer: Circle) -> None:
        """Generating the atrium in the center of the map

        Args:
            height (int | float): Floor height
            outer (Circle): Outer circle
        """
        center = Circle(radius=4, points=32, bounds=(30, -30%360))
        self.load(Center, "Central staircase", height=height, outer=center)
        for bounds in ((0, 180), (180, 360)):
            self.load(AtriumFloor, "Atrium floor", height=height, outer=outer(bounds=bounds), inner=center(bounds=bounds))



class Babel(Object):
    """Implementation of the Tower of Babel map
    """

    def generate(self, height: int|float = 5) -> None:
        """Generating a floor of a tower of Babel

        Args:
            height (int | float, optional): Floor height. Defaults to 5.
        """
        atrium = Circle(10, 64)
        self.load(Atrium, "Atrium", height=height, outer=atrium)



if __name__ == "__main__":
    Blender.setup()
    Blender.purge()
    Babel("Tower of Babel").print().build()
    #Babel("Tower of Babel (above copy)", V3.UP * 5).build()
    #Babel("Tower of Babel (below copy)", V3.DOWN * 5).build()