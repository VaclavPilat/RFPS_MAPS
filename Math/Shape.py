## \file
# Implementations of shapes and and their vertex generation
from Math.Functions import Math
from Math.Vector import V3
from Utils.Wrapper import autoRepr, immutable
import math



@immutable
@autoRepr
class Circle:
    """Data object for storing information used for generating points in circles

    Made immutable and has an automatic __repr__() implementation by using decorators
    """

    def __init__(self, radius: int|float = 1, points: int = 8, pivot: V3 = V3.ZERO, bounds: tuple = None) -> None:
        """Initializing an Circle instance

        Args:
            radius (int | float, optional): Circle radius, in meters. Defaults to 1.
            points (int, optional): Number of points in circle, should be a power of 2. Defaults to 8.
            pivot (V3, optional): Circle pivot point. Defaults to V3.ZERO.
            bounds (tuple, optional): Pair of angle bound values in degrees. Defaults to None.
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
        if bounds is not None:
            assert len(bounds) == 2, "Exactly 2 bounds are required"
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