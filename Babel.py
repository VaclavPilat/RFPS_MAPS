## \file
# Implementation of the Babel map
if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from Math.Vector import V3
from Math.Interval import I360
from Math.Shape import Circle
from Blender.Object import Object
from Blender.Blender import Blender



class Column(Object):
    """Cylinder mesh with vertical walls only
    """

    def generate(self, height: int|float, circle: Circle) -> None:
        """Generating a column

        Args:
            height (int | float): Column height.
            circle (Circle): Column radius.
        """
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
        for face in inner.cylinder(height, closed=False):
            self.face(face, inverted=True)
        # Walls between outer and inner
        #self.face([outer_upper[0], inner_upper[0], inner_lower[0], outer_lower[0]])
        #self.face([inner_upper[-1], outer_upper[-1], outer_lower[-1], inner_lower[-1]])



class SpiralStairs(Object):
    """Spiral staircase
    """

    def generate(self, height: int|float, outer: Circle, inner: Circle) -> None:
        """Generating a spiral staircase

        Args:
            height (int|float): Floor height
            outer (Circle): Outer circle
            inner (Circle): inner circle
        """
        outer_vertices, inner_vertices = (x for x in (outer.vertices(), inner.vertices()))
        outer_edges, inner_edges = (len(x) - 1 for x in (outer_vertices, inner_vertices))
        steps = inner_edges
        print(steps)



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
        column = Circle(radius=1, points=outer.points)
        self.load(Column, "Central pillar", height=height, circle=column)
        self.load(CenterWall, "Central wall", height=height, outer=outer, inner=inner)
        self.load(SpiralStairs, "Spiral stairs", height=height, outer=inner, inner=column(bounds=inner.bounds))



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
        center = Circle(radius=4, points=32, bounds=I360(30, -30%360))
        self.load(Center, "Central staircase", height=height, outer=center)
        for bounds in (I360(0, 180), I360(180, 360)):
            self.load(AtriumFloor, "Atrium floor", height=height, outer=outer(bounds=bounds), inner=center(bounds=bounds))
        #for position in Circle(radius=Math.average(outer.radius, center.radius), points=8.vertices():
        #    self.load(Column, "Atrium pillar", height=3, circle=Circle(0.5, 8, position))



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