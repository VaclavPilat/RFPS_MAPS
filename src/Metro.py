## \file
# Implementation of the Metro station map
if __name__ == "__main__":
    try:
        import os, sys, bpy
        IN_BLENDER = True
        directory = os.path.dirname(bpy.data.filepath)
        if not directory in sys.path:
            sys.path.append(directory)
    except ImportError:
        IN_BLENDER = False
from Math.Vector import V3
from Blender.Object import createObjectSubclass, Object
from Utils.Decorators import defaultKwargsValues, makeImmutable
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
def Slopes(self, depth: float) -> None:
    LTR, LBR = map(lambda x: x + V3.DOWN * depth, (self.TR, self.BR))
    self.face(LTR, self.TL, self.BL, LBR)
    self.face(self.TR, self.TL, LTR)
    self.face(self.BL, self.BR, LBR)
    


@createObjectSubclass(Object)
def Metro(self) -> None:
    """Generating the Metro station
    """
    for i in range(4):
        self.load(Slopes, "Test", V3.ZERO, 3, 3, rotation=i, depth=3)



if __name__ == "__main__":
    if IN_BLENDER:
        from Blender.Functions import setupForDevelopment, purgeExistingObjects
        setupForDevelopment()
        purgeExistingObjects()
    metro = Metro("Metro station")
    metro.print()
    if IN_BLENDER:
        metro.build()