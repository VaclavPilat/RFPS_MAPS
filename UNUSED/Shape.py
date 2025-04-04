## \file
# Implementations of shapes and their vertex generation
from Math.Vector import V3
from Math.Interval import I360
from Math.Functions import isPow2
from Utils.Decorators import addInitRepr, makeImmutable, addCopyCall
import math



# noinspection PyCallingNonCallable
@makeImmutable
@addInitRepr
@addCopyCall("radius", "pivot", "bounds")
## \todo Refactor & add docs
class Circle:
    """Data object for storing information used for generating points in circles

    Made immutable and has an automatic __repr__() implementation by using decorators
    """

    def __init__(self, radius: int|float = 1, pivot: V3 = V3.ZERO, bounds: I360 = I360(openEnd=True)) -> None:
        """Initializing a Circle instance

        Args:
            radius (int | float, optional): Circle radius, in meters. Defaults to 1.
            pivot (V3, optional): Circle pivot point. Defaults to V3.ZERO.
            bounds (I360, optional): Angle bound values in degrees. Defaults to I360().
        """
        ## Circle radius
        assert radius > 0, "Radius has to be a positive number"
        self.radius = radius
        ## Position of the center of the circle
        self.pivot = pivot
        ## Generated circle bounds
        self.bounds = bounds
    
    ## \todo Change start/end generation so that both of these points are the lines which were cut off rather than on the circle itself
    def __iter__(self):
        """Generating vertex points on a circle
        """
        for degree in self.bounds:
            radians = math.radians(degree)
            sin = math.sin(radians)
            cos = math.cos(radians)
            yield self.pivot + (V3.FORWARD * sin + V3.RIGHT * cos) * self.radius
    
    def __pos__(self) -> list:
        """Returning a list of generated vertices

        Returns:
            list: List of generated vertex positions
        """
        return list(self)
    
    def cylinder(self, height: int|float, closed: bool = True):
        """Generating cylinder walls

        Args:
            height (int | float): Cylinder height
            closed (bool, optional): Should the cylinder be closed? Defaults to True.

        Yields:
            tuple: Sequences of vertices for each face
        """
        lower = tuple(self)
        upper = tuple(self(pivot=self.pivot + V3.UP * height))
        for i, j in [(a-1, a) for a in range(not closed, len(lower))]:
            yield upper[j], upper[i], lower[i], lower[j]
    
    def face(self, cutout: "Circle" = None) -> tuple:
        """Generating circle face

        Args:
            cutout (Circle, optional): Circular hole dimensions. Defaults to None.

        Returns:
            tuple: Sequence of vertices
        """
        if cutout is None:
            return tuple(self)
        assert cutout.radius < self.radius, "A hole has to be smaller that the object it is a part of!"
        return tuple(self) + tuple(cutout)[::-1]
    
    def gap(self, gap: int|float) -> "Circle":
        """Create a new circle with a hole the size of the gap

        Args:
            gap (int | float): Gap size

        Returns:
            Circle: New circle with correct interval values
        """
        angle = round(math.degrees(math.asin(gap/2 / self.radius)))
        return self(bounds=I360(angle, 360-angle, points=self.bounds.points))