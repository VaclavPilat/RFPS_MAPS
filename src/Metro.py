## \file
# Implementation of the Metro station map
if __name__ == "__main__":
    import os, sys, bpy
    directory = os.path.dirname(bpy.data.filepath)
    if not directory in sys.path:
        sys.path.append(directory)
from Math.Vector import V3
from Blender.Object import createObjectSubclass, Object
from Utils.Decorators import defaultKwargsValues, makeImmutable
from enum import Enum



class Pivot(Enum):
    """Enum for tile bound generation
    """

    TOP_LEFT = 0
    TOP = 1
    TOP_RIGHT = 2
    LEFT = 3
    CENTER = 4
    RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM = 7
    BOTTOM_RIGHT = 8



class Tile(Object):
    """Base class for all Metro Objects
    """

    def __init__(self, name: str, position: V3, width: float, height: float, pivot: Pivot = Pivot.TOP_LEFT, rotation: int = 0) -> None:
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
        super().__init__(name, position)
    
    def rotate(self, point: V3) -> V3:
        """Rotating a point around tile pivot

        Args:
            point (V3): Point to rotate

        Returns:
            V3: Rotated point
        """
        return ((point - self.position) >> self.rotation) + self.position



@createObjectSubclass(Tile)
def Rectangle(self) -> None:
    """Simple rectangle
    """
    self.face(self.TR, self.TL, self.BL, self.BR)



@createObjectSubclass(Object)
def Metro(self) -> None:
    """Generating the Metro station
    """
    self.load(Rectangle, "Test", V3.ZERO, 2, 1)



if __name__ == "__main__":
    from Blender.Functions import setupForDevelopment, purgeExistingObjects
    setupForDevelopment()
    purgeExistingObjects()
    Metro("Metro station").print().build()