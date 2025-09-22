"""! \file
Implementation of the Metro station map
"""
from src.Decorators import addInitRepr
from src.Mesh import Vector, Face, ZERO, ONE, FORWARD, BACKWARD, LEFT, RIGHT, UP, DOWN
from src.Objects import Object, createObjectSubclass
import decimal, enum


# Setting up decimal
decimal.getcontext().prec = 6 # Setting precision to 6 decimal places
decimal.getcontext().Emin = 0 # Disabling negative exponents, meaning that all values will be rounded to the preset precision
decimal.getcontext().traps[decimal.FloatOperation] = True # Forbidding interactions between decimals and floats


@addInitRepr
class Tile(Object):
    """Object subclass representing a tile.
    """

    def __init__(self, name: str = "New tile", position: Vector = ZERO, size: Vector = ONE, pivot: Vector = ZERO,
                 rotation: int = 0, *args, **kwargs) -> None:
        """Initializing a Tile instance

        Args:
            name (str, optional): Object name. Defaults to "New tile".
            position (Vector, optional): Object position. Defaults to ZERO.
            size (Vector, optional): Object size in meters. Defaults to ONE.
            pivot (Vector, optional): Relative pivot position within the object, with values from -1 to 1. Defaults to CENTER.
        """
        if any(map(lambda value: value < 0, size)):
            raise ValueError("Tile size cannot be negative")
        if size == ZERO:
            raise ValueError("Tile size cannot be zero")
        if not all(map(lambda value: -1 <= value <= 1, pivot)):
            raise ValueError("Pivot values must be between -1 and 1")
        normalized = Vector(*map(lambda value: (value + 1) / decimal.Decimal(2), pivot))
        midpoint = size ** normalized
        ## Tile bound sizes, from the object position (pivot)
        self.bounds = tuple(zip(midpoint, size - midpoint))
        # noinspection PyArgumentList
        super().__init__(name, position, rotation, *args, **kwargs)

    def __getitem__(self, point: Vector) -> Vector:
        """Getting the positions of a point from within the tile size

        Args:
            point (Vector): Relative pivot position within the bounding box

        Returns:
            Vector: Position of the point
        """
        if not all(map(lambda value: -1 <= value <= 1, point)):
            raise ValueError("Point values must be between -1 and 1")
        return Vector(*map(lambda axis: axis[0] * axis[1][axis[0] >= 0], zip(point, self.bounds)))


@createObjectSubclass(Tile)
def Test(self):
    self += Face(self[FORWARD+RIGHT], self[FORWARD+LEFT], self[BACKWARD+LEFT], self[BACKWARD+RIGHT])


from src.Grids import Grid
Grid(Test())()


import sys
sys.exit()


## \file
# Implementation of the Metro station map.
# \todo Refactor
if __name__ == "__main__":
    try:
        # noinspection PyUnresolvedReferences
        import os, sys, bpy

        BLENDER = True
        directory = os.path.dirname(bpy.data.filepath)
        if not directory in sys.path:
            sys.path.append(directory)
    except ImportError:
        BLENDER = False

from src.Mesh import FORWARD, BACKWARD, LEFT, RIGHT, UP, DOWN, ZERO, Face
from src.Grids import Grid

from src import Tiles, Helpers
from src.Objects import createObjectSubclass


## Setting constants used in the Metro map
METRO = Helpers.Settings(
    UECH=0.1,  # Underpass entrance curb height (in meters)
    UECW=0.3,  # Underpass entrance curb width (in meters)
    UEWD=3,  # Underpass entrance width (in meters)
    UHDP=1,  # Underpass hallway depth (in meters)
    UHHG=3,  # Underpass hallway height (in meters)
    UHWD=5,  # Underpass hallway width (in meters)
    USCL=10,  # Underpass staircase length (in meters)
    USLC=3,  # Underpass slope count
    USLL=37,  # Underpass slope length (in meters)
    USLR=8,  # Underpass slope ratio
    USTG=3,  # Underpass step group count
    USTH=0.2,  # Underpass step height (in meters)
    USTL=0.3,  # Underpass step length (in meters)
)


# noinspection PyIncorrectDocstring,PyPep8Naming
@createObjectSubclass(Tiles.Tile)
def Stairs(self, D: float, G: int, H: float, L: float) -> None:
    """Generating multiple flights of stairs with resting places in between

    Args:
        D (float): Total staircase depth (in meters)
        G (int): Number of step groups
        H (float): Step height (in meters, will be adjusted)
        L (float): Step length (in meters)
    """
    assert G >= 1, "At least 1 step group required"
    VF = round(D / H)  # Vertical face count
    HF = VF + 1  # Horizontal face count
    assert HF * L < self.bounds.width, "Steps will not fit horizontally"
    TL, BL = (self.bounds.TL, self.bounds.BL)
    if G >= 2:
        R = (self.bounds.width - (HF - G + 1) * L) / (G - 1)  # Resting place length
    I = set(int(i / G * HF) for i in range(1, G))  # Resting place indices
    for i in range(HF):
        if i == HF - 1:  # Final horizontal face
            self += Face(self.bounds.TR(z=TL.z), TL, BL, self.bounds.BR(z=BL.z))
            break
        # Making a horizontal face
        TL1, BL1 = map(lambda v: v + RIGHT * (R if i in I else L), (TL, BL))
        self += Face(TL1, TL, BL, BL1)
        # Making a vertical face
        z = (self.bounds.TL + DOWN * D * (i + 1) / VF).z
        TL2, BL2 = map(lambda v: v(z=z), (TL1, BL1))
        self += Face(TL2, TL1, BL1, BL2)
        TL, BL = (TL2, BL2)


# noinspection PyIncorrectDocstring,PyPep8Naming
@createObjectSubclass(Tiles.Tile)
def Slopes(self, D: float, S: int, R: float) -> None:
    """Generating multiple (wheelchair accessible) slopes with resting places in between

    Args:
        D (float): Total depth (in meters)
        S (int): Slope count
        R (float): Slope ratio (slope length per meter of descent)
    """
    assert S >= 1, "At least 1 slope is required"
    assert D * R < self.bounds.width, "Slopes would not fit horizontally"
    if S > 1:
        G = (self.bounds.width - D * R) / (S - 1)  # Resting place (gap) length
    TL, BL = (self.bounds.TL, self.bounds.BL)
    C = 1 if S == 1 else S - 1  # Resting place count
    for i in range(S + C):
        if i > 0 and i == S + C - 1:  # Final face, whatever it might be
            self += Face(TL, BL, *map(lambda v: v + DOWN * D, (self.bounds.BR, self.bounds.TR)))
            break
        if i % 2 == 0:  # Making a slope face
            z = (self.bounds.TL + DOWN * D * (i // 2 + 1) / S).z
            TL1, BL1 = map(lambda v: (v + RIGHT * (TL.z - z) * R)(z=z), (TL, BL))
        else:  # Making a horizontal face
            TL1, BL1 = map(lambda v: v + RIGHT * G, (TL, BL))
        self += Face(TL1, TL, BL, BL1)
        TL, BL = (TL1, BL1)


# noinspection PyIncorrectDocstring,PyPep8Naming
@createObjectSubclass(Tiles.Tile)
def UnderpassEntrance(self, C: type = None, **kwargs) -> None:
    """Generating an underpass entrance

    Args:
        C (type, optional): Class for generating descent. Defaults to None.
    """
    TLI, TRI = map(lambda v: v + BACKWARD * METRO.UECW, (self.bounds.TL, self.bounds.TR))
    BLI, BRI = map(lambda v: v + FORWARD * METRO.UECW, (self.bounds.BL, self.bounds.BR))
    TRI, BRI = map(lambda v: v + LEFT * METRO.UECW, (TRI, BRI))
    TL1, TR1, BL1, BR1 = map(lambda v: v + UP * METRO.UECH,
                             (self.bounds.TL, self.bounds.TR, self.bounds.BL, self.bounds.BR))
    TLI1, TRI1, BLI1, BRI1 = map(lambda v: v + UP * METRO.UECH, (TLI, TRI, BLI, BRI))
    self += Face(TR1, TL1, TLI1, TRI1, BRI1, BLI1, BL1, BR1)  # Top face
    # Outer faces
    self += Face(TR1, BR1, self.bounds.BR, self.bounds.TR)
    self += Face(TL1, TR1, self.bounds.TR, self.bounds.TL)
    self += Face(BR1, BL1, self.bounds.BL, self.bounds.BR)
    self += Face(TLI1, TL1, self.bounds.TL, TLI)
    self += Face(BL1, BLI1, BLI, self.bounds.BL)
    # Inner faces
    self += Face(BLI1, BRI1, BRI, BLI)
    self += Face(BRI1, TRI1, TRI, BRI)
    self += Face(TRI1, TLI1, TLI, TRI)
    # Generating descending mesh
    if C is not None:
        self += C(f"Underpass {str(C).lower()}", Tiles.Anchor(TLI, BRI), D=METRO.UHDP + METRO.UHHG, **kwargs)


# noinspection PyUnresolvedReferences
@createObjectSubclass()
def Metro(self) -> None:
    """Generating the Metro station
    """
    self += UnderpassEntrance("Underpass stair entrance", Tiles.Box(ZERO, METRO.USCL, METRO.UEWD),
              C=Stairs, G=METRO.USTG, H=METRO.USTH, L=METRO.USTL)
    #self += UnderpassEntrance("Underpass slope entrance", Tiles.Box(BACKWARD * METRO.UEWD + RIGHT *
    #    (METRO.USCL + METRO.UHWD + METRO.USLL), METRO.USLL, METRO.UEWD, rotation=180),
    #    C=Slopes, S=METRO.USLC, R=METRO.USLR)


if __name__ == "__main__":
    # noinspection PyTypeChecker
    metro = Metro("Metro station")
    # noinspection PyUnboundLocalVariable,IncorrectFormatting
    if BLENDER:
        from src import Blender
        Blender.Setup.purge()
        Blender.Setup.development()
        # noinspection PyTypeChecker
        Blender.Objects.build(metro)
    else:
        Grid(metro, 10)()
        print(metro)