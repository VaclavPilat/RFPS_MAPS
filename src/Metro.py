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
from Utils.Decorators import defaultKwargsValues, makeImmutable
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
    
    def gridAxis(self, axis: str) -> tuple:
        """Getting axis information

        Args:
            axis (str): Axis name (x/y/z)

        Returns:
            tuple: Tuple (axis values, differences, min difference, just)
        """
        values = sorted(set(getattr(vertex, axis) for face in self.faces for vertex in face))
        differences = [values[i] - values[i-1] for i in range(1, len(values))]
        minimum = min(differences)
        just = max(map(lambda value: len(str(value)), values))
        return (values, differences, minimum, just)
    
    def grid(self) -> str:
        """Getting a string representation of an object in a grid view

        Returns:
            str: Grid representation of this object as a string
        """
        Xvals, Xdiff, Xmin, Xjust = self.gridAxis("x")
        Yvals, Ydiff, Ymin, Yjust = self.gridAxis("y")
        Yvals.reverse()
        Ydiff.reverse()
        # Header
        for i in range(Yjust + 1):
            output = " " * (Xjust + 2)
            for j, y in enumerate(Yvals):
                if j > 0:
                    output += " " * (Ydiff[j-1] // Ymin)
                output += (str(y).rjust(Yjust) + "╷")[i]
            print(output)
        # Body
        for x in Xvals:
            output = str(x).rjust(Xjust) + "╶╌"
            for j, y in enumerate(Yvals):
                if j > 0:
                    output += "╌" * (Ydiff[j-1] // Ymin)
                output += "┼"
            output += "╌╴" + str(x)
            print(output)
        # Footer
        for i in range(Yjust + 1):
            output = " " * (Xjust + 2)
            for j, y in enumerate(Yvals):
                if j > 0:
                    output += " " * (Ydiff[j-1] // Ymin)
                output += ("╵" + str(y).ljust(Yjust))[i]
            print(output)



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
    for i in range(1):
        print(self.load(Slopes, "Test", V3.ZERO, 3, 3, rotation=i, depth=3).grid())



if __name__ == "__main__":
    if BLENDER:
        from Blender.Functions import setupForDevelopment, purgeExistingObjects
        setupForDevelopment()
        purgeExistingObjects()
    metro = Metro("Metro station")
    print(metro.hierarchy())
    if BLENDER:
        metro.build()