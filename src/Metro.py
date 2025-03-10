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
    TOP_LEFT = 0

    ## Top right corner
    TOP_RIGHT = 1

    ## Bottom left corner
    BOTTOM_LEFT = 2

    ## Bottom right corner
    BOTTOM_RIGHT = 3



@addInitRepr
class Tile(Object):
    """Base class for all Metro Objects
    """

    def __init__(self, name: str, position: V3, width: float, height: float, pivot: Pivot = Pivot.TOP_LEFT, rotation: int = 0, *args, **kwargs) -> None:
        """Initialising a Metro tile

        Args:
            name (str): Tile name
            position (V3): Tile position
            width (float): Tile width
            height (float): tile height
            pivot (Pivot, optional): Pivot point. Defaults to Pivot.TOP_LEFT.
            rotation (int, optional): Rotation index. Defaults to 0.
        """
        ## Tile width
        self.width = width
        ## Tile height
        self.height = height
        ## Pivot point
        self.pivot = pivot
        ## Rotation index
        self.rotation = rotation
        # Calculating bounds
        if self.pivot == Pivot.TOP_LEFT:
            self.TL = position
            self.TR = position + V3.RIGHT * width
            self.BL = position + V3.BACKWARD * height
            self.BR = self.BL + V3.RIGHT * width
        else:
            raise ValueError("Unexpected Pivot value")
        super().__init__(name, position, *args, **kwargs)
    
    def rotate(self, point: V3) -> V3:
        """Rotating a point around tile pivot

        Args:
            point (V3): Point to rotate

        Returns:
            V3: Rotated point
        """
        return ((point - self.position) >> self.rotation) + self.position
    
    def face(self, *points, **kwargs) -> None:
        """Rotating face around tile pivot
        """
        points = list(map(self.rotate, points))
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
    assert HF * L < self.width, "Steps will not fit horizontally"
    TL, BL = (self.TL, self.BL)
    if G >= 2:
        R = (self.width - (HF - G + 1) * L) / (G - 1) # Resting place length
    I = set(int(i / G * HF) for i in range(1, G)) # Resting place indices
    for i in range(HF):
        if i == HF - 1: # Final horizontal face
            self.face(self.TR(z=TL.z), TL, BL, self.BR(z=BL.z))
            break
        # Making a horizontal face
        TL1, BL1 = map(lambda v: v + V3.RIGHT * (R if i in I else L), (TL, BL))
        self.face(TL1, TL, BL, BL1)
        # Making a vertical face
        z = (self.TL + V3.DOWN * D * (i + 1) / VF).z
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
    assert D * R < self.width, "Slopes would not fit horizontally"
    G = (self.width - D * R) / (S - 1) # Resting place (gap) length
    TL, BL = (self.TL, self.BL)
    for i in range(S):
        # Making a slope face
        z = (self.TL + V3.DOWN * D * (i + 1) / S).z
        TL1, BL1 = map(lambda v: (v + V3.RIGHT * (TL.z - z) * R)(z=z), (TL, BL))
        self.face(TL1, TL, BL, BL1)
        # Making a horizontal face
        TL2, BL2 = map(lambda v: v + V3.RIGHT * G, (TL1, BL1))
        self.face(TL2, TL1, BL1, BL2)
        TL, BL = (TL2, BL2)



@createObjectSubclass(Object)
def Metro(self) -> None:
    """Generating the Metro station
    """
    self.load(Stairs, "Underpass entrance stairs", V3.ZERO, 10, 3, D=4)
    self.load(Slopes, "Underpass entrance slopes", V3.BACKWARD * 3, 40, 3, D=4).printGrids()



if __name__ == "__main__":
    if BLENDER:
        from Blender.Functions import setupForDevelopment, purgeExistingObjects
        setupForDevelopment()
        purgeExistingObjects()
    metro = Metro("Metro station")
    metro.printHierarchy()
    if BLENDER:
        metro.build()