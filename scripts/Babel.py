"""! \file
Implementation of the Tower of Babel map.
"""
from src.Decorators import makeImmutable, addInitRepr, addCopyCall
from src.Intervals import Interval, FULL
from src.Mesh import Vector, Face, ZERO, ONE, FORWARD, BACKWARD, LEFT, RIGHT, UP, DOWN
from src.Objects import createObjectSubclass
import math, decimal


# Setting up decimal
decimal.getcontext().prec = 6 # Setting precision to 6 decimal places
decimal.getcontext().Emin = 0 # Disabling negative exponents, meaning that all values will be rounded to the preset precision
decimal.getcontext().traps[decimal.FloatOperation] = True # Forbidding interactions between decimals and floats


## Babel team side count
BTC = 3
assert 2 <= BTC
## Babel floor height
BFH = decimal.Decimal("5")
## Babel doorway height
BDH = decimal.Decimal("3")
## Atrium wall segment count (including doorways)
AWC: int = 12
assert AWC % BTC == 0
## Atrium doorway count (could be either a hallway or entrance to team side)
ADC = 6
assert AWC % ADC == 0
assert ADC % BTC == 0
## Atrium floor radius (in meters)
AFR = decimal.Decimal("15")


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


@createObjectSubclass()
def Atrium(self):
    self += Face(*Circle(points=AWC, radius=AFR))


from src.Grids import Grid, Highlight, Scale, Direction
Grid(Atrium("Atrium"), 100, highlight=Highlight.VERTICES, scale=Scale.JOINT, direction=Direction.TOP)()