## \file
# Implementation of a Tile mesh object
from Math.Vector import V3
from Mesh.Object import Object
from Utils.Decorators import defaultKwargsValues, makeImmutable, addInitRepr
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