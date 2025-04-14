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

    def __init__(self, origin: V3, TL: V3, BR: V3, rotation: int = 0) -> None:
        """Initialising Tile boundaries

        Args:
            origin (V3): Tile origin (pivot) point (relative to parent's origin)
            TL (V3): Top left tile corner (relative to parent's origin)
            BR (V3): Bottom right tile corner (relative to parent's origin)
            rotation (int, optional): Rotation index. Defaults to 0.
        """
        ## Tile origin (pivot) point (relative to parent's origin)
        self.origin = origin
        ## Top left tile corner position (relative to origin)
        assert TL.z == BR.z, "All bounds have to have the same z-value"
        self.TL = TL - origin
        ## Bottom right tile corner position (relative to origin)
        self.BR = BR - origin
        ## Top right tile corner position (relative to origin)
        self.TR = self.TL(y=self.BR.y)
        ## Bottom left tile corner position (relative to origin)
        self.BL = self.TL(x=self.BR.x)
        ## Tile rotation index as a value from 0 to 3
        self.rotation = rotation
        ## Tile width (in meters)
        self.width = abs(self.TL - self.TR)
        assert self.width > 0, "Tile width has to be positive"
        ## Tile height (in meters)
        self.height = abs(self.TL - self.BL)
        assert self.height > 0, "Tile height has to be positive"

    def rotate(self, point: V3) -> V3:
        """Rotating a vertex point around tile pivot

        Args:
            point (V3): Vertex position to rotate (relative to origin)

        Returns:
            V3: Rotated vertex position (relative to origin)
        """
        return point >> self.rotation


@addInitRepr
class Box(Bounds):
    """Class for representing a bounding box of a Tile
    """

    def __init__(self, origin: V3, width: float, height: float, rotation: int = 0, pivot: Pivot = Pivot.TL) -> None:
        """Initialising a bounding box

        Args:
            origin (V3): Tile origin (pivot) point (relative to parent's origin)
            width (float): Tile width (in meters)
            height (float): Tile height (in meters)
            rotation (int, optional): Rotation index. Defaults to 0.
            pivot (Pivot, optional): Pivot location. Defaults to Pivot.TL.
        """
        if pivot == Pivot.TL:
            TL = origin
            BR = TL + V3.RIGHT * width + V3.BACKWARD * height
        else:
            raise ValueError("Unexpected Pivot value")
        # noinspection PyArgumentList
        super().__init__(origin, TL, BR, rotation)


@addInitRepr
class Anchor(Bounds):
    """Class for representing anchor bounds of a Tile
    """

    def __init__(self, TL: V3, BR: V3, pivot: Pivot = Pivot.TL, rotation: int = 0) -> None:
        """Initialising anchor bounds

        Args:
            TL (V3): Top left tile corner (relative to parent's origin)
            BR (V3): Bottom right tile corner (relative to parent's origin)
            pivot (Pivot, optional): Pivot location. Defaults to Pivot.TL.
            rotation (int, optional): Rotation index. Defaults to 0.
        """
        if pivot == Pivot.TL:
            origin = TL
        else:
            raise ValueError("Unexpected Pivot value")
        # noinspection PyArgumentList
        super().__init__(origin, TL, BR, rotation)


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
        super().__init__(name, position=bounds.origin, rotation=V3.UP * bounds.rotation * 90, *args, **kwargs)

    #def face(self, *points, **kwargs) -> None:
    #    """Rotating face around tile pivot
    #    """
    #    points = list(map(self.bounds.rotate, points))
    #    super().face(*points, **kwargs)