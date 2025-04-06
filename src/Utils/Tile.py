## \file
# Implementation of a Tile mesh object
from .Object import Object
from .Vector import V3
from .Decorators import makeImmutable, addInitRepr
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


# noinspection PyCallingNonCallable
@makeImmutable
class Bounds:
    """Class for representing Tile bounds
    """

    def __init__(self, O: V3, TL: V3, BR: V3, R: int = 0) -> None:
        """Initialising Tile boundaries

        Args:
            O (V3): Tile origin (pivot) point (relative to parent's origin)
            TL (V3): Top left tile corner (relative to parent's origin)
            BR (V3): Bottom right tile corner (relative to parent's origin)
            R (int, optional): Rotation index. Defaults to 0.
        """
        ## Tile origin (pivot) point (relative to parent's origin)
        self.O = O
        ## Top left tile corner position (relative to origin)
        assert TL.z == BR.z, "All bounds have to have the same z-value"
        self.TL = TL - O
        ## Bottom right tile corner position (relative to origin)
        self.BR = BR - O
        ## Top right tile corner position (relative to origin)
        self.TR = self.TL(y=self.BR.y)
        ## Bottom left tile corner position (relative to origin)
        self.BL = self.TL(x=self.BR.x)
        ## Tile rotation index as a value from 0 to 3
        self.R = R
        ## Tile width (in meters)
        self.W = abs(self.TL - self.TR)
        assert self.W > 0, "Tile width has to be positive"
        ## Tile height (in meters)
        self.H = abs(self.TL - self.BL)
        assert self.H > 0, "Tile height has to be positive"

    def rotate(self, point: V3) -> V3:
        """Rotating a vertex point around tile pivot

        Args:
            point (V3): Vertex position to rotate (relative to origin)

        Returns:
            V3: Rotated vertex position (relative to origin)
        """
        return point >> self.R


@addInitRepr
class Box(Bounds):
    """Class for representing a bounding box of a Tile
    """

    def __init__(self, O: V3, W: float, H: float, P: Pivot = Pivot.TL, R: int = 0) -> None:
        """Initialising a bounding box

        Args:
            O (V3): Tile origin (pivot) point (relative to parent's origin)
            W (float): Tile width (in meters)
            H (float): Tile height (in meters)
            P (Pivot, optional): Pivot location. Defaults to Pivot.TL.
            R (int, optional): Rotation index. Defaults to 0.
        """
        if P == Pivot.TL:
            TL = O
            BR = TL + V3.RIGHT * W + V3.BACKWARD * H
        else:
            raise ValueError("Unexpected Pivot value")
        # noinspection PyArgumentList
        super().__init__(O, TL, BR, R)


@addInitRepr
class Anchor(Bounds):
    """Class for representing anchor bounds of a Tile
    """

    def __init__(self, TL: V3, BR: V3, P: Pivot = Pivot.TL, R: int = 0) -> None:
        """Initialising anchor bounds

        Args:
            TL (V3): Top left tile corner (relative to parent's origin)
            BR (V3): Bottom right tile corner (relative to parent's origin)
            P (Pivot, optional): Pivot location. Defaults to Pivot.TL.
            R (int, optional): Rotation index. Defaults to 0.
        """
        if P == Pivot.TL:
            O = TL
        else:
            raise ValueError("Unexpected Pivot value")
        # noinspection PyArgumentList
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
        # noinspection PyTypeChecker
        super().__init__(name, position=self.bounds.O, rotation=V3.UP * bounds.R * 90, *args, **kwargs)

    #def face(self, *points, **kwargs) -> None:
    #    """Rotating face around tile pivot
    #    """
    #    points = list(map(self.bounds.rotate, points))
    #    super().face(*points, **kwargs)