"""! \file
Functionality for rendering Object meshes in console.

Presenting 3D objects as 2D renders from specified directions and with other customizable settings.

\todo Add an option to show bounding boxes of objects
"""
from .Decorators import makeImmutable
from .Mesh import Vector, Line, ZERO
from .Objects import Object
from .Colors import Color, Temperature, alen
import enum, sys


class Shape (enum.IntFlag):
    """Flags for the shape of a vertex character shown in View

    Examples:
        >>> str(Shape.TOP | Shape.BOTTOM | Shape.LEFT)
        '┫'
    """

    ## Contains no lines
    NONE = 0
    ## Contains top line
    TOP = 1
    ## Contains right line
    RIGHT = 2
    ## Contains bottom line
    BOTTOM = 4
    ## Contains left line
    LEFT = 8

    def __str__(self) -> str:
        """Getting a character representing vertex point shape

        Returns:
            str: String representation of vertex point

        Examples:
            >>> str(Shape.NONE)
            '┼'
        """
        return "┼╹╺┗╻┃┏┣╸┛━┻┓┫┳╋"[self]


class Axis (enum.Enum):
    """Enum for representing either positive or negative axis
    """

    ## Positive X axis
    X = 1
    ## Positive Y axis
    Y = 2
    ## Positive Z axis
    Z = 3
    ## Negative X axis
    _X = -1
    ## Negative Y axis
    _Y = -2
    ## Negative Z axis
    _Z = -3

    def __init__(self, value: int) -> None:
        """Initialising an Axis instance
        """
        ## Line representing axis direction
        self.line = Line(ZERO, Vector(**{str(self).lower(): value}))

    def __bool__(self) -> bool:
        """Checking whether the axis is positive or negative

        Returns:
            bool: True if the axis is positive

        Examples:
            >>> bool(Axis.X)
            True
            >>> bool(Axis._X)
            False
        """
        return self.value > 0

    def __neg__(self) -> "Axis":
        """Changing axis from positive to negative or vice versa

        Returns:
            Axis: Negated axis

        Examples:
            >>> -Axis.X == Axis._X
            True
        """
        return Axis(-self.value)

    def __str__(self) -> str:
        """Getting a character representing axis name

        Returns:
            str: Character representing axis name

        Examples:
            >>> str(Axis.Y) == str(Axis._Y)
            True
        """
        return self.name[-1]

    # noinspection PyCallingNonCallable
    def __call__(self, vector: Vector) -> float:
        """Getting the value of a vector that corresponds to self axis

        Args:
            vector (Vector): Vector to get the axis value of

        Returns:
            float: Axis value

        Examples:
            >>> Axis.Z(Vector(1, 2, 3))
            3
            >>> Axis._Y(Vector(1, 2, 3))
            2
        """
        return getattr(vector, str(self).lower())


class Direction (enum.IntFlag):
    """Flag representing the directions an Object can be rendered from
    """

    ## Top view direction
    TOP = 1, -Axis.X, -Axis.Y, Color.Z
    ## Front view direction
    FRONT = 2, -Axis.Z, -Axis.Y, Color.X
    ## Side view direction
    SIDE = 4, -Axis.Z, Axis.X, Color.Y

    def __new__(cls, value: int, vertical: Axis, horizontal: Axis, color: Color = Color.NONE) -> "Direction":
        """Creating a new instance of Direction

        Args:
            value (int): Direction value
            vertical (Axis): Vertical axis
            horizontal (Axis): Horizontal axis
            color (Color, optional): Color representing the direction. Defaults to Color.NONE.
        """
        member = int.__new__(cls, value)
        member._value_ = value
        member.vertical = vertical
        member.horizontal = horizontal
        member.color = color
        return member

    def __iter__(self):
        """Getting strings representing the direction.

        Works only when the value is "canonical" (single bit).
        """
        top = (f"╺{'╋━━'[::1 if self.horizontal else -1]}╸", f"{Color[str(self.horizontal)](self.horizontal)}", " ")
        middle = (" ", "┃", "     ")
        bottom = (" ", f"{Color[str(self.vertical)](self.vertical)}", "     ")
        for line in (top, middle, bottom)[::1 if self.vertical else -1]:
            yield "".join(line[::1 if self.horizontal else -1])


class Highlight (enum.Enum):
    """Enums for adjusting vertex and line colors indexes
    """

    ## Colorizing vertices based on their counts and disregarding line counts
    VERTICES = (
        lambda vertex, top, right, bottom, left: vertex,
        lambda line: 0,
        Color.MAGENTA
    )
    ## Colorizing vertices based on neighbouring line counts
    EDGES = (
        lambda vertex, top, right, bottom, left: next((x for x in (top, bottom, left, right) if x), 0),
        lambda line: line,
        Color.CYAN
    )

    def __init__(self, point, line, color: Color = Color.NONE) -> None:
        """Initialising a Highlight instance

        Args:
            point: Function for updating color index for points
            line: Function for updating color index for lines
            color (Color, optional): Color representing the highlight. Defaults to Color.NONE.
        """
        ## Function for adjusting point count
        self.point = point
        ## Function for adjusting line count
        self.line = line
        ## Color representing the highlight
        self.color = color


class Scale (enum.Enum):
    """Enum for the scale of axis values.

    Members are one-value tuples due to the fact that lambdas as enum values alone don't work.
    """

    ## Both axis have independent scales
    INDEPENDENT = lambda this, other: this, Color.YELLOW
    ## Both axis have the same scales
    JOINT = lambda this, other: min(this, other), Color.GREEN

    def __init__(self, increment, color: Color = Color.NONE) -> None:
        """Initialising a Scale instance

        Args:
            increment: Function for selecting a scale increment
            color (Color, optional): Color representing the scale. Defaults to Color.NONE.
        """
        ## Function for selecting a scale increment
        self.increment = increment
        ## Color representing the scale
        self.color = color

    def __call__(self, this: float, other: float) -> float:
        """Updating the minimal increment (render scale) of the current axis

        Args:
            this (float): Minimal increment on the current axis
            other (float): Minimal increment on the other axis

        Returns:
            Resulting increment on the current axis
        """
        return self.value[0](this, other)


@makeImmutable
class Header:
    """Class for providing basic information on an Object that is being rendered
    """

    def __init__(self, obj: Object, depth: int, counts: dict, direction: Direction, highlight: Highlight, scale: Scale) -> None:
        """Initializing a Header

        Args:
            obj (Object): Object that is being described
            depth (int): Maximum rendering depth
            counts (dict): Dictionary of vertex, line and face counts
            direction (Direction): Direction from which the object is being rendered
            highlight (Highlight): What part of the object is to be highlighted
            scale (Scale): Render axis scale
        """
        ## Render direction lines
        self.direction = list(direction)
        ## Info strings
        self.info = (
            # First column
            f"{Color.BOLD(obj.name)}" + (f" (+{Temperature(depth)(depth)} layers deep)" if depth else ""),
            " ".join(f"{temp(i if i != len(Temperature) - 1 else f'{i}+')}" for i, temp in enumerate(Temperature)),
            # Second column
            f"{direction.color(direction.name)} view of {highlight.color(highlight.name)} with {scale.color(scale.name)} scale",
            ", ".join(f"{Temperature(value)(value)} {key if value != 1 else key[:-1]}" for key, value in counts.items()),
        )

    def __str__(self) -> str:
        """Getting a string representation of a grid header

        Returns:
             str: ANSI colored string representation of a grid header
        """
        lines = [f"┌{'─' * 7}", *(f"│{line}" for line in self.direction), f"└{'─' * 7}"]
        for i in range((len(self.info) + 1) // 2):
            just = max(map(alen, self.info[i * 2:i * 2 + 2]))
            for j in range(5):
                lines[j] += f"┬│{'┼' if i else '├'}│┴"[j]
                index = i * 2 + j // 2
                if j % 2 == 0:
                    lines[j] += "─" * (just + 2)
                elif index < len(self.info):
                    lines[j] += f" {self.info[index]}{' ' * (just - alen(self.info[index]) + 1)}"
                else:
                    lines[j] += " " * (just + 2)
        return "\n".join(line + f"┐│{'┤' if self.info else '│'}│┘"[i] for i, line in enumerate(lines))


## \todo Refactor
class Values:
    """Class for containing detailed information on axis values
    """

    def __init__(self, axis: Axis, vertices: tuple, multiplier: int = 1) -> None:
        """Initializing Values instance.

        Multiplier is needed due to the fact that monospaced fonts used in consoles have a size ratio of 1:2.
        Using a multiplier makes sure that same-size shapes, like squares and circles do not look overtly stretched.

        Args:
            axis (Axis): Axis that these values belong to
            vertices (tuple): Transformed vertex positions
            multiplier (int, optional): Offset size multiplier. Defaults to 1.
        """
        ## Axis
        self.axis = axis
        ## Value offset multiplier
        self.multiplier = multiplier
        ## Axis values
        self.values = sorted(set(map(axis, vertices)), reverse=not axis)
        ## Axis value labels
        self.labels = tuple(map(lambda value: str(round(value, 3)), self.values))
        ## Label justify length
        self.just = max(map(lambda value: len(str(value)), self.labels))
        ## Value increments
        self.differences = tuple(map(lambda pair: abs(pair[0] - pair[1]), zip(self.values, self.values[1:])))
        ## Minimal value increment
        self.minimum = min(self.differences) if self.differences else sys.maxsize
        if self.minimum < 0.0001:
            raise ValueError("Mesh contains floating point errors")

    def __call__(self, minimum: float) -> None:
        """Settting the offsets between axis values by supplying an updated divisor (minimum increment)

        Args:
            minimum (float): Updated increment divisor
        """
        ## Axis value offsets
        self.offsets = tuple(map(lambda d: round(d / minimum) * self.multiplier - 1, self.differences))


@makeImmutable
## \todo Refactor
class Render:
    """Class for rendering 3D object(s) as a 2D view
    """

    def __init__(self, mesh: dict, direction: Direction, highlight: Highlight, scale: Scale) -> None:
        """Initialising a Render instance

        Args:
            mesh (dict): Transformed mesh vertices and edges
            direction (Direction): Direction from which to render the mesh
            highlight (Highlight): What part of the mesh will be highlighted
            scale (Scale): Render axis scale
        """
        ## Transformed object mesh
        self.mesh = mesh
        ## Render direction
        self.direction = direction
        ## Highlighted part of the render
        self.highlight = highlight
        ## Horizontal axis values
        self.horizontal = Values(direction.horizontal, mesh["vertices"], 2)
        ## Vertical axis values
        self.vertical = Values(direction.vertical, mesh["vertices"])
        self.horizontal(scale.increment(self.horizontal.minimum, self.vertical.minimum))
        self.vertical(scale.increment(self.vertical.minimum, self.horizontal.minimum))


@makeImmutable
## \todo Refactor
class Grid:
    """Class for rendering 3D object(s) as a 2D text grid into stdout
    """

    def __init__(self, obj: Object, depth: int = 0) -> None:
        """Initialising a Grid instance

        Args:
            obj (Object): 3D object whose mesh will be rendered
            depth (int, optional): Maximum object depth that will be rendered. Defaults to 0.
        """
        # Object to be rendered
        self.obj = obj
        # Maximum rendering depth
        self.depth = depth
        # Precalculated object counts
        self.counts = self.count(obj, depth)
        # Pretransformed object mesh
        self.mesh = self.transform(obj, depth)

    def count(self, obj: Object, depth: int) -> dict:
        """Counting faces, edges and vertices of a specified object (recursively)

        Args:
            obj (Object): Object whose mesh structure is being counted
            depth (int): Remaining recursion depth

        Returns:
            dict: Dictionary of Blender-like vertex, edge and face counts
        """
        counts = {
            "objects": 1,
            "vertices": len(set(vertex for face in obj.faces for vertex in face.points)),
            "edges": len(set(line for face in obj.faces for line in face)),
            "faces": len(obj.faces),
            "triangles": sum(len(face) - 2 for face in obj.faces),
        }
        if depth > 0:
            for child in obj.objects:
                for key, value in self.count(child, depth - 1).items():
                    counts[key] += value
        return counts

    def transform(self, obj: Object, depth: int) -> dict:
        """Getting transformed mesh data of a specified object (recursively)

        Args:
            obj (Object): Object whose mesh is being transformed
            depth (int): Remaining recursion depth

        Returns:
            dict: Dictionary of transformed Blender-like vertex and edge positions
        """
        data = {
            "vertices": tuple(set(vertex for face in obj.faces for vertex in face.points)),
            "edges": tuple(set(line for face in obj.faces for line in face)),
        }
        if depth > 0:
            for child in obj.objects:
                for key, value in self.transform(child, depth - 1).items():
                    data[key] += value
        for key, value in data.items():
            data[key] = tuple(map(obj.__matmul__, value))
        return data

    def __call__(self, directions: Direction = Direction.TOP | Direction.FRONT | Direction.SIDE,
                 highlight: Highlight = Highlight.EDGES, scale: Scale = Scale.INDEPENDENT, header: bool = True) -> None:
        """Printing the object render into stdout

        Args:
            directions (Direction, optional): Direction(s) from which to render the object.
                Defaults to Direction.TOP | Direction.FRONT | Direction.SIDE.
            highlight (Highlight, optional): Which part of the render to highlight? Defaults to Highlight.EDGES.
            scale (Scale, optional): Render axis scale. Defaults to Scale.INDEPENDENT.
            header (bool, optional): Should basic information about the render be included as a header in the print?
        """
        for direction in Direction:
            if direction in directions:
                if header:
                    print(Header(self.obj, self.depth, self.counts, direction, highlight, scale))
                print(Render(self.mesh, direction, highlight, scale))