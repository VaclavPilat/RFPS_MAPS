## \file
# Implementations of shapes and and their vertex generation
## \todo Rename file to Shapes
from Math.Data import V3, Interval
from Utils.Decorators import addInitRepr, makeImmutable, addCopyCall
import math



@makeImmutable
@addInitRepr
@addCopyCall("radius", "points", "pivot", "bounds")
class Circle:
    """Data object for storing information used for generating points in circles

    Made immutable and has an automatic __repr__() implementation by using decorators
    """

    def __init__(self, radius: int|float = 1, points: int = 8, pivot: V3 = V3.ZERO, bounds: Interval = None) -> None:
        """Initializing an Circle instance

        Args:
            radius (int | float, optional): Circle radius, in meters. Defaults to 1.
            points (int, optional): Number of points in circle, should be a power of 2. Defaults to 8.
            pivot (V3, optional): Circle pivot point. Defaults to V3.ZERO.
            bounds (Interval, optional): Angle bound values in degrees. Defaults to None.
        """
        ## Circle radius
        assert radius > 0, "Radius has to be a positive number"
        self.radius = radius
        ## Number of points on the whole circle
        assert points > 0, "Point count has to be a positive number"
        self.points = points
        ## Position of the center of the circle
        self.pivot = pivot
        ## Generated circle bounds
        ## \todo Make it possible to create Circle instances with bounds like (330-30)
        self.bounds = bounds
    
    def vertices(self) -> tuple:
        """Generating vertex points on a circle

        Returns:
            tuple: Tuple of generated vertex positions
        """
        ## \todo Change start/end generation so that both of these points are the lines which were cut off rather than on the circle itself
        if self.bounds is None:
            degrees = [360 * i / self.points for i in range(self.points)]
        else:
            degrees = [d for d in [360 * i / self.points for i in range(self.points + 1)] if d in self.bounds]
        radians = [math.radians(d) for d in degrees]
        return tuple(self.pivot + (V3.FORWARD * math.sin(r) + V3.RIGHT * math.cos(r)) * self.radius for r in radians)
    
    def cylinder(self, height: int|float, closed: bool = True):
        """Generating cylinder walls

        Args:
            height (int | float): Cylinder height
            closed (bool, optional): Should the cylinder be closed? Defaults to True.

        Yields:
            tuple: Sequences of vertices for each face
        """
        lower = self.vertices()
        upper = self(pivot=self.pivot + V3.UP * height).vertices()
        for i, j in [(a-1, a) for a in range(not closed, len(lower))]:
            yield (upper[j], upper[i], lower[i], lower[j])
    
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