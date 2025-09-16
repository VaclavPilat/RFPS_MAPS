"""! \file
Implementation of the Tower of Babel map.
"""
from src.Decorators import makeImmutable, addInitRepr, addCopyCall
from src.Intervals import Interval, FULL
from src.Mesh import Vector, ZERO, FORWARD, RIGHT, Face
from src.Objects import createObjectSubclass
import math


@makeImmutable
@addInitRepr
@addCopyCall("origin", "radius", "arc", "points", "sin", "cos")
class Circle:
    """Class for storing information necessary to render a simple circle.
    """

    def __init__(self, origin: Vector = ZERO, radius: float = 1, arc: Interval = FULL, points: int = 8,
                 sin: Vector = FORWARD, cos: Vector = RIGHT):
        """Initialising a Circle instance.

        Args:
            origin (Vector, optional): Origin (pivot) point of the circle. Defaults to ZERO.
            radius (float, optional): Circle radius, in meters. Defaults to 1.
            arc (Interval, optional): Which part of the circle should the points be generated in. Defaults to FULL.
            points (int, optional): Number of points in the circle. Defaults to 8.
            sin (Vector, optional): Direction of sinus. Defaults to FORWARD.
            cos (Vector, optional): Direction of cosinus. Defaults to RIGHT.
        """
        ## Origin point
        self.origin = origin
        ## Circle radius
        self.radius = radius
        ## Circular interval for generating points
        self.arc = arc
        ## Number of points on the whole circle
        self.points = points
        ## Sinus direction
        self.sin = sin
        ## Cosinus direction
        self.cos = cos

    ## \todo Figure out how to do this with Decimal and float trap or fixed decimal place count
    def __iter__(self):
        """Generating points on a circle.

        Sinus and cosinus outputs are currently rounded to 5 decimal places.
        """
        for angle in self.arc[self.points]:
            radians = math.radians(angle)
            yield self.origin + self.sin * round(math.sin(radians), 5) + self.cos * round(math.cos(radians), 5)


@createObjectSubclass()
def CircleTest(self):
    self += Face(*Circle())


from src.Grids import Grid, Highlight, Scale
Grid(CircleTest("Circle test"), 100, highlight=Highlight.VERTICES, scale=Scale.JOINT)()