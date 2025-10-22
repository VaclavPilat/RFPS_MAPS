"""! \file
Implementation of the Tower of Babel map.
"""
if __name__ == "__main__":
    # Enabling module imports when the script is being run from Blender. DO NOT REMOVE.
    try:
        # noinspection PyUnresolvedReferences
        import bpy, os, sys
        directory = os.path.dirname(bpy.data.filepath)
        if not directory in sys.path:
            sys.path.append(directory)
    except ImportError:
        pass


from src.Decorators import makeImmutable, addInitRepr, addCopyCall
from src.Intervals import Interval, FULL
from src.Mesh import Vector, Face, ZERO, ONE, FORWARD, BACKWARD, LEFT, RIGHT, UP, DOWN
from src.Objects import createObjectSubclass
import math, decimal


# Setting up decimal
decimal.getcontext().prec = 6 # Setting precision to 6 decimal places
decimal.getcontext().Emin = 0 # Disabling negative exponents, meaning that all values will be rounded to the preset precision
decimal.getcontext().traps[decimal.FloatOperation] = True # Forbidding interactions between decimals and floats


class BABEL:
    """Various constants related to the Tower of Babel map
    """

    ## Team side count
    teamCount: int = 3
    assert 2 <= teamCount
    ## Babel floor height, in meters
    floorHeight: decimal.Decimal = decimal.Decimal("5")
    ## Babel doorway height, in meters
    doorHeight: decimal.Decimal = decimal.Decimal("3")

    ## Atrium wall segment count (including doorways)
    atriumWalls: int = 12
    assert atriumWalls % teamCount == 0
    ## Atrium doorway count (could be either a hallway or entrance to team side)
    atriumDoors: int = 6
    assert atriumWalls % atriumDoors == 0
    assert atriumDoors % teamCount == 0
    ## Atrium floor radius, in meters
    atriumRadius: decimal.Decimal = decimal.Decimal("15")

    ## Pillar radius, in meters
    pillarRadius: decimal.Decimal = decimal.Decimal("0.5")
    ## Pillar face count
    pillarSegments: int = 16


@makeImmutable
@addInitRepr
@addCopyCall("origin", "radius", "arc", "points", "sin", "cos")
class Circle:
    """Class for storing information necessary to render a simple circle.

    Calculations are meant to be done with decimal.Decimal instances instead of floats to avoid floating point errors.
    By floating point errors I mean axis having values differing less than epsilon.
    """

    def __init__(self, origin: Vector = ZERO, radius: decimal.Decimal = decimal.Decimal(1), arc: Interval = FULL,
                 points: int = 8, sin: Vector = FORWARD, cos: Vector = RIGHT):
        """Initialising a Circle instance.

        Args:
            origin (Vector, optional): Origin (pivot) point of the circle. Defaults to ZERO.
            radius (decimal.Decimal, optional): Circle radius, in meters. Defaults to decimal.Decimal(1).
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
        """Generating points on a circle.
        """
        for angle in self.arc[self.points]:
            radians = math.radians(angle)
            sin = decimal.getcontext().create_decimal_from_float(math.sin(radians))
            cos = decimal.getcontext().create_decimal_from_float(math.cos(radians))
            yield self.origin + (self.sin * sin + self.cos * cos) * self.radius

    def __getitem__(self, i: int) -> Vector:
        return tuple(self)[i % self.points]


@createObjectSubclass()
def Pillar(self, radius: decimal.Decimal, height: decimal.Decimal, segments: int) -> None:
    """Generating a pillar from the object's origin

    Args:
        radius (decimal.Decimal): Pillar radius
        height (decimal.Decimal): Pillar height
        segments (int): Number of faces on the pillar
    """
    lower = Circle(radius=radius, points=segments)
    upper = lower(origin=UP * height)
    for i in range(segments):
        self += Face(upper[i], upper[i-1], lower[i-1], lower[i])


@createObjectSubclass()
def Atrium(self):
    lower = Circle(points=BABEL.atriumWalls, radius=BABEL.atriumRadius)
    upper = lower(origin=UP*BABEL.floorHeight)
    self += Face(*lower)
    for i in range(BABEL.atriumWalls):
        if i % BABEL.atriumDoors > 0:
            self += Face(upper[i-1], upper[i], lower[i], lower[i-1])


if __name__ == "__main__":
    map = Atrium("Atrium")
    try:
        from src.Blender import Setup, Objects
        Setup.purge()
        Setup.development()
        Objects.build(map)
    except ImportError:
        from src.Grids import Grid, Highlight, Scale, Direction
        Grid(map, 100, highlight=Highlight.VERTICES, scale=Scale.JOINT, direction=Direction.TOP)()