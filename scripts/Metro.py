"""! \file
Implementation of the Metro station map
"""
if __name__ == "__main__":
    # Enabling module imports when the script is being run from Blender
    try:
        # noinspection PyUnresolvedReferences
        import bpy, os, sys
        directory = os.path.dirname(bpy.data.filepath)
        if not directory in sys.path:
            sys.path.append(directory)
    except ImportError:
        pass


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

        Allows for the translation of direction vectors (for example, FORWARD+LEFT) into their respective positions.
        This means that `Tile[BOTTOM+RIGHT+FORWARD]` will return the position of the bottom-right-forward corner of the
        tile, regardless of the pivot position.

        Args:
            point (Vector): Relative pivot position within the bounding box

        Returns:
            Vector: Position of the point
        """
        if not all(map(lambda value: -1 <= value <= 1, point)):
            raise ValueError("Point values must be between -1 and 1")
        return Vector(*map(lambda axis: axis[0] * axis[1][axis[0] >= 0], zip(point, self.bounds)))


class METRO:
    """Class for containing various constants related to the Metro station map
    """

    ## Underpass hallway depth, in meters
    UHD = decimal.Decimal("1")
    ## Underpass hallway height, in meters
    UHH = decimal.Decimal("3")
    ## Underpass hallway width, in meters
    UHW = decimal.Decimal("3")
    ## Underpass entrance width, in meters
    UEW = decimal.Decimal("3")
    ## Underpass stair entrance length, in meters
    UST = decimal.Decimal("5")
    ## Underpass slope entrance length, in meters
    USL = decimal.Decimal("15")
    ## Underpass curb width, in meters
    UCW = decimal.Decimal("0.3")
    ## Underpass curb height, in meters
    UCH = decimal.Decimal("0.2")


@createObjectSubclass(Tile)
def UnderpassEntrance(self, width: decimal.Decimal = METRO.UCW):
    # Getting point coordinates
    ULF = self[UP + LEFT + FORWARD]
    ULB = self[UP + LEFT + BACKWARD]
    URF = self[UP + RIGHT + FORWARD]
    URB = self[UP + RIGHT + BACKWARD]
    DLF = self[DOWN + LEFT + FORWARD]
    DLB = self[DOWN + LEFT + BACKWARD]
    DRF = self[DOWN + RIGHT + FORWARD]
    DRB = self[DOWN + RIGHT + BACKWARD]
    ULFI, DLFI, URFI, DRFI = [point + BACKWARD * width for point in (ULF, DLF, URF, DRF)]
    ULBI, DLBI, URBI, DRBI = [point + FORWARD * width for point in (ULB, DLB, URB, DRB)]
    URFI, DRFI, URBI, DRBI = [point + LEFT * width for point in (URFI, DRFI, URBI, DRBI)]
    # Creating faces
    self += Face(ULF, URF, DRF, DLF)
    self += Face(URF, URB, DRB, DRF)
    self += Face(URB, ULB, DLB, DRB)
    self += Face(ULB, ULBI, DLBI, DLB)
    self += Face(ULFI, ULF, DLF, DLFI)
    self += Face(ULBI, URBI, DRBI, DLBI)
    self += Face(URFI, ULFI, DLFI, DRFI)
    self += Face(URBI, URFI, DRFI, DRBI)
    self += Face(ULB, URB, URF, ULF, ULFI, URFI, URBI, ULBI)


if __name__ == "__main__":
    # noinspection PyNoneFunctionAssignment
    metro = UnderpassEntrance(pivot=DOWN+FORWARD+LEFT, size=Vector(METRO.UEW, METRO.UST, METRO.UCH))
    try:
        from src.Blender import Setup, Objects
        Setup.purge()
        Setup.development()
        # noinspection PyTypeChecker
        Objects.build(metro)
    except ImportError:
        from src.Grids import Grid, Direction, Highlight, Scale
        for direction in Direction:
            Grid(metro, 5, direction=direction, scale=Scale.NONE, highlight=Highlight.EDGES)()