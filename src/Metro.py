## \file
# Implementation of the Metro station map
if __name__ == "__main__":
    try:
        import os, sys, bpy
        BLENDER = True
        directory = os.path.dirname(bpy.data.filepath)
        if not directory in sys.path:
            sys.path.append(directory)
    except ImportError:
        BLENDER = False
from Math.Vector import V3
from Mesh.Object import createObjectSubclass
from Utils.Decorators import defaultKwargsValues, makeImmutable, addInitRepr
if BLENDER:
    from Blender.Object import Object
else:
    from Mesh.Object import Object
from enum import Enum



class Pivot(Enum):
    """Enum for containing all pivot types of a Tile.

    Pivot is the origin point of a Tile instance.
    Tile is built and rotated around a pivot.
    """

    ## Top left corner
    TL = 0

    ## Top right corner
    TR = 1

    ## Bottom left corner
    BL = 2

    ## Bottom right corner
    BR = 3



@makeImmutable
class Bounds:
    """Class for representing Tile bounds
    """

    def __init__(self, O: V3, TL: V3, BR: V3, R: int = 0) -> None:
        """Initialising Tile boundaries

        Args:
            O (V3): Tile origin (pivot) point
            TL (V3): Top left tile corner
            BR (V3): Bottom right tile corner
            R (int, optional): Rotation index. Defaults to 0.
        """
        ## Tile origin (pivot) point
        self.O = O
        ## Top left tile corner
        assert TL.z == BR.z, "All bounds have to have the same z-value"
        self.TL = TL
        ## Top right tile corner
        self.TR = TL(y=BR.y)
        ## Bottom left tile corner
        self.BL = TL(x=BR.x)
        ## Bottom right tile corner
        self.BR = BR
        ## Tile rotation index
        self.R = R
        ## Tile width
        self.W = abs(self.TL - self.TR)
        assert self.W > 0, "Tile width has to be positive"
        ## Tile height
        self.H = abs(self.TL - self.BL)
        assert self.H > 0, "Tile height has to be positive"

    def rotate(self, point: V3) -> V3:
        """Rotating a vertex point around tile pivot

        Args:
            point (V3): Point to rotate

        Returns:
            V3: Rotated vertex position
        """
        return self.O + ((point - self.O) >> self.R)



@addInitRepr
class Box(Bounds):
    """Class for representing a bounding box of a Tile
    """

    def __init__(self, O: V3, W: float, H: float, P: Pivot = Pivot.TL, R: int = 0) -> None:
        """Initialising a bounding box

        Args:
            O (V3): Tile origin (pivot) point
            W (float): Tile width
            H (float): Tile height
            P (Pivot, optional): Pivot location. Defaults to Pivot.TL.
            R (int, optional): Rotation index. Defaults to 0.
        """
        if P == Pivot.TL:
            TL = O
            BR = TL + V3.RIGHT * W + V3.BACKWARD * H
        else:
            raise ValueError("Unexpected Pivot value")
        super().__init__(O, TL, BR, R)



@addInitRepr
class Anchor(Bounds):
    """Class for representing anchor bounds of a Tile
    """

    def __init__(self, TL: V3, BR: V3, P: Pivot = Pivot.TL, R: int = 0) -> None:
        """Initialising anchor bounds

        Args:
            TL (V3): Top left tile corner
            BR (V3): Bottom right tile corner
            P (Pivot, optional): Pivot location. Defaults to Pivot.TL.
            R (int, optional): Rotation index. Defaults to 0.
        """
        if P == Pivot.TL:
            O = TL
        else:
            raise ValueError("Unexpected Pivot value")
        super().__init__(O, TL, BR, R)



@addInitRepr
class Tile(Object):
    """Base class for all Metro Objects
    """

    def __init__(self, name: str, bounds: Bounds, *args, **kwargs) -> None:
        """Initialising a Metro tile

        Args:
            name (str): Tile name
            bounds (Bounds): Tile boundaries
        """
        ## Tile boundaries
        self.bounds = bounds
        super().__init__(name, self.bounds.O, *args, **kwargs)
    
    def face(self, *points, **kwargs) -> None:
        """Rotating face around tile pivot
        """
        points = list(map(self.bounds.rotate, points))
        super().face(*points, **kwargs)



@createObjectSubclass(Tile)
def Stairs(self, D: float, G: int = 3, H: float = 0.2, L: float = 0.3) -> None:
    """Generating multiple flights of stairs with resting places in between

    Args:
        D (float): Total staircase depth (in meters)
        G (int, optional): Number of step groups. Defaults to 3.
        H (float, optional): Step height (in meters, will be adjusted). Defaults to 0.2.
        L (float, optional): Step length (in meters). Defaults to 0.3.
    """
    assert G >= 1, "At least 1 step group required"
    VF = round(D / H) # Vertical face count
    HF = VF + 1 # Horizontal face count
    assert HF * L < self.bounds.W, "Steps will not fit horizontally"
    TL, BL = (self.bounds.TL, self.bounds.BL)
    if G >= 2:
        R = (self.bounds.W - (HF - G + 1) * L) / (G - 1) # Resting place length
    I = set(int(i / G * HF) for i in range(1, G)) # Resting place indices
    for i in range(HF):
        if i == HF - 1: # Final horizontal face
            self.face(self.bounds.TR(z=TL.z), TL, BL, self.bounds.BR(z=BL.z))
            break
        # Making a horizontal face
        TL1, BL1 = map(lambda v: v + V3.RIGHT * (R if i in I else L), (TL, BL))
        self.face(TL1, TL, BL, BL1)
        # Making a vertical face
        z = (self.bounds.TL + V3.DOWN * D * (i + 1) / VF).z
        TL2, BL2 = map(lambda v: v(z=z), (TL1, BL1))
        self.face(TL2, TL1, BL1, BL2)
        TL, BL = (TL2, BL2)



@createObjectSubclass(Tile)
def Slopes(self, D: float, S: int = 3, R: float = 8) -> None:
    """Generating multiple (wheelchair accessible) slopes with resting places in between

    Args:
        D (float): Total depth (in meters)
        S (int, optional): Slope count. Defaults to 3.
        R (float, optional): Slope ratio (slope length per meter of descent). Defaults to 8.
    """
    assert S >= 1, "At least 1 slope is required"
    assert D * R < self.bounds.W, "Slopes would not fit horizontally"
    if S > 1:
        G = (self.bounds.W - D * R) / (S - 1) # Resting place (gap) length
    TL, BL = (self.bounds.TL, self.bounds.BL)
    C = 1 if S == 1 else S - 1 # Resting place count
    for i in range(S + C):
        if i > 0 and i == S + C - 1: # Final face, whatever it might be
            self.face(TL, BL, *map(lambda v: v + V3.DOWN * D, (self.bounds.BR, self.bounds.TR)))
            break
        if i % 2 == 0: # Making a slope face
            z = (self.bounds.TL + V3.DOWN * D * (i // 2 + 1) / S).z
            TL1, BL1 = map(lambda v: (v + V3.RIGHT * (TL.z - z) * R)(z=z), (TL, BL))
        else: # Making a horizontal face
            TL1, BL1 = map(lambda v: v + V3.RIGHT * G, (TL, BL))
        self.face(TL1, TL, BL, BL1)
        TL, BL = (TL1, BL1)



@createObjectSubclass(Tile)
def UnderpassEntrance(self, H: float = 0.1, W: float = 0.3) -> None:
    """Generating an underpass entrance

    Args:
        H (float, optional): Curb height (in meters). Defaults to 0.1.
        W (float, optional): Curb width (in meters). Defaults to 0.3.
    """
    TLI, TRI = map(lambda v: v + V3.BACKWARD * W, (self.bounds.TL, self.bounds.TR))
    BLI, BRI = map(lambda v: v + V3.FORWARD * W, (self.bounds.BL, self.bounds.BR))
    TRI, BRI = map(lambda v: v + V3.LEFT * W, (TRI, BRI))
    TL1, TR1, BL1, BR1 = map(lambda v: v + V3.UP * H, (self.bounds.TL, self.bounds.TR, self.bounds.BL, self.bounds.BR))
    TLI1, TRI1, BLI1, BRI1 = map(lambda v: v + V3.UP * H, (TLI, TRI, BLI, BRI))
    self.face(TR1, TL1, TLI1, TRI1, BRI1, BLI1, BL1, BR1) # Top face
    # Outer faces
    self.face(TR1, BR1, self.bounds.BR, self.bounds.TR)
    self.face(TL1, TR1, self.bounds.TR, self.bounds.TL)
    self.face(BR1, BL1, self.bounds.BL, self.bounds.BR)
    self.face(TLI1, TL1, self.bounds.TL, TLI)
    self.face(BL1, BLI1, BLI, self.bounds.BL)
    # Inner faces
    self.face(BLI1, BRI1, BRI, BLI)
    self.face(BRI1, TRI1, TRI, BRI)
    self.face(TRI1, TLI1, TLI, TRI)



@createObjectSubclass(Object)
def Metro(self) -> None:
    """Generating the Metro station
    """
    self.load(Stairs, "Underpass entrance stairs", Box(V3.ZERO, 10, 3), D=4)
    self.load(Slopes, "Underpass entrance slopes", Box(V3.BACKWARD * 3, 40, 3), D=4)
    self.load(UnderpassEntrance, "Underpass entrance", Box(V3.ZERO, 10, 3)).printGrids()



if __name__ == "__main__":
    if BLENDER:
        from Blender.Functions import setupForDevelopment, purgeExistingObjects
        setupForDevelopment()
        purgeExistingObjects()
    metro = Metro("Metro station")
    metro.printHierarchy()
    if BLENDER:
        metro.build()