## \file
# Implementation of a Tile mesh object.
# Tiles are Objects that are rectangle-shaped (without specifying height).
# \todo Refactor and add tests
from .Mesh import *
from .Objects import Object
from . import Decorators
import enum


class Pivot(enum.Enum):
    """Enum for containing all pivot types of a Tile.

    Pivot is the origin point of a Tile instance.
    Tile is built and rotated around a pivot.
    """
    ## Center of the tile
    CENTER = 0
    ## Top left tile corner
    TOP_LEFT = 1
    ## Top right tile corner
    TOP_RIGHT = 2
    ## Bottom left tile corner
    BOTTOM_LEFT = 3
    ## Bottom right tile corner
    BOTTOM_RIGHT = 4


# noinspection PyCallingNonCallable
@Decorators.makeImmutable
class Bounds:
    """Class for representing Tile bounds
    """

    def __init__(self, origin: Vector, TL: Vector, BR: Vector, rotation: int = 0) -> None:
        """Initialising Tile boundaries

        Args:
            origin (Vector): Tile origin (pivot) point (relative to parent's origin)
            TL (Vector): Top left tile corner (relative to parent's origin)
            BR (Vector): Bottom right tile corner (relative to parent's origin)
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

    def rotate(self, point: Vector) -> Vector:
        """Rotating a vertex point around tile pivot

        Args:
            point (Vector): Vertex position to rotate (relative to origin)

        Returns:
            Vector: Rotated vertex position (relative to origin)
        """
        return point >> self.rotation


@Decorators.addInitRepr
class Box(Bounds):
    """Class for representing a bounding box of a Tile by its size
    """

    def __init__(self, origin: Vector, width: float, height: float, rotation: int = 0, pivot: Pivot = Pivot.TOP_LEFT) -> None:
        """Initialising a bounding box

        Args:
            origin (Vector): Tile origin (pivot) point (relative to parent's origin)
            width (float): Tile width (in meters)
            height (float): Tile height (in meters)
            rotation (int, optional): Rotation index. Defaults to 0.
            pivot (Pivot, optional): Pivot location. Defaults to Pivot.TOP_LEFT.
        """
        if pivot == Pivot.TOP_LEFT:
            TL = origin
            BR = TL + RIGHT * width + BACKWARD * height
        else:
            raise ValueError("Unexpected Pivot value")
        # noinspection PyArgumentList
        super().__init__(origin, TL, BR, rotation)


@Decorators.addInitRepr
class Anchor(Bounds):
    """Class for representing anchor bounds of a Tile by its corner positions
    """

    def __init__(self, TL: Vector, BR: Vector, rotation: int = 0, pivot: Pivot = Pivot.TOP_LEFT) -> None:
        """Initialising anchor bounds

        Args:
            TL (Vector): Top left tile corner (relative to parent's origin)
            BR (Vector): Bottom right tile corner (relative to parent's origin)
            rotation (int, optional): Rotation index. Defaults to 0.
            pivot (Pivot, optional): Pivot location. Defaults to Pivot.TOP_LEFT.
        """
        if pivot == Pivot.TOP_LEFT:
            origin = TL
        else:
            raise ValueError("Unexpected Pivot value")
        # noinspection PyArgumentList
        super().__init__(origin, TL, BR, rotation)


@Decorators.addInitRepr
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
        super().__init__(name, position=bounds.origin, rotation=bounds.rotation, *args, **kwargs)