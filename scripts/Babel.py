from src.Decorators import makeImmutable
from src.Intervals import Interval, FULL
from src.Mesh import Vector, ZERO, FORWARD, RIGHT
import math


@makeImmutable
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

    def __iter__(self):
        """Generating points on a circle
        """
        for angle in self.arc[self.points]:
            radians = math.radians(angle)
            yield self.origin + self.sin * math.sin(radians) + self.cos * math.cos(radians)