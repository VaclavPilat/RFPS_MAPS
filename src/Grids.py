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


## \todo Figure out how to render an object from multiple directions (possbly with some shenanigans in Grid.__new__?)
class Direction (enum.Enum):
    """Flag representing the directions an Object can be rendered from
    """

    ## Top view direction
    TOP = -Axis.X, -Axis.Y, Color.Z
    ## Front view direction
    FRONT = -Axis.Z, -Axis.Y, Color.X
    ## Side view direction
    SIDE = -Axis.Z, Axis.X, Color.Y

    def __init__(self, vertical: Axis, horizontal: Axis, color: Color = Color.NONE) -> None:
        """Initialising a Direction instance

        Args:
            vertical (Axis): Vertical axis
            horizontal (Axis): Horizontal axis
            color (Color, optional): Color representing the direction. Defaults to Color.NONE.
        """
        ## Vertical axis
        self.vertical = vertical
        ## Horizontal axis
        self.horizontal = horizontal
        ## Color representing the direction
        self.color = color

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
class Grid:
    """Class for storing settings for rendering 3D objects as 2D views
    """

    def __init__(self, obj: Object, depth: int = 0, direction: Direction = Direction.SIDE,
                 highlight: Highlight = Highlight.EDGES, scale: Scale = Scale.INDEPENDENT, header: bool = True) -> None:
        """Initialising a Grid instance

        Args:
            obj (Object): 3D object whose mesh will be rendered
            depth (int, optional): Maximum object depth that will be rendered. Defaults to 0.
            direction (Direction, optional): Direction(s) from which to render the object. Defaults to Direction.TOP.
            highlight (Highlight, optional): Which part of the render to highlight? Defaults to Highlight.EDGES.
            scale (Scale, optional): Render axis scale. Defaults to Scale.INDEPENDENT.
            header (bool, optional): Should basic information about the render be included as a header in the print?
        """
        ## Object to render
        self.obj = obj
        ## Maximum rendering depth
        self.depth = depth
        ## Direction to render from
        self.direction = direction
        ## What part of the render to highlight
        self.highlight = highlight
        ## Axis value scale
        self.scale = scale
        ## Should a header be shown?
        self.header = header

    def __str__(self) -> str:
        """Getting a string representing the grid render

        Returns:
            str: Grid render string with header (if enabled)
        """
        return (f'{Header(self)}\n' if self.header else '') + str(Render(self))

    def __call__(self) -> None:
        """Printing the object render into stdout
        """
        print(self)


@makeImmutable
class Header:
    """Class for providing basic information on an Object that is being rendered
    """

    def __init__(self, grid: Grid) -> None:
        """Initializing a Header

        Args:
            grid (Grid): Grid settings
        """
        ## Grid settings to describe
        self.grid = grid

    def __call__(self, obj: Object, depth: int = 0) -> tuple:
        """Counting faces, edges and vertices of a specified object (recursively)

        Args:
            obj (Object): Object whose mesh structure is being counted
            depth (int, optional): Current recursion depth. Defaults to 0.

        Returns:
            tuple: Maximum reached depth and dict with structural counts
        """
        counts = {
            "objects": 1,
            "vertices": len(set(vertex for face in obj.faces for vertex in face.points)),
            "edges": len(set(line for face in obj.faces for line in face)),
            "faces": len(obj.faces),
            "triangles": sum(len(face) - 2 for face in obj.faces),
        }
        maxDepth = depth
        if depth < self.grid.depth:
            for child in obj.objects:
                childDepth, childCounts = self(child, depth + 1)
                maxDepth = max(maxDepth, childDepth)
                for key, value in childCounts.items():
                    counts[key] += value
        return maxDepth, counts

    def __iter__(self):
        """Yielding information strings to be shown in the header
        """
        depth, counts = self(self.grid.obj)
        # First column
        yield f"{Color.BOLD(self.grid.obj.name)}" + (f" (+{Temperature(depth)(depth)} layers deep)" if depth else "")
        yield " ".join(f"{temp(i if i != len(Temperature) - 1 else f'{i}+')}" for i, temp in enumerate(Temperature))
        # Second column
        yield (f"{self.grid.direction.color(self.grid.direction.name)} view"
               f" of {self.grid.highlight.color(self.grid.highlight.name)}"
               f" with {self.grid.scale.color(self.grid.scale.name)} scale")
        yield ", ".join(f"{Temperature(value)(value)} {key if value != 1 else key[:-1]}" for key, value in counts.items())

    def __str__(self) -> str:
        """Getting a string representation of a grid header

        Returns:
             str: ANSI colored string representation of a grid header
        """
        info = list(self)
        lines = [f"┌{'─' * 7}", *(f"│{line}" for line in list(self.grid.direction)), f"└{'─' * 7}"]
        for i in range((len(info) + 1) // 2):
            just = max(map(alen, info[i * 2:i * 2 + 2]))
            for j in range(5):
                lines[j] += f"┬│{'┼' if i else '├'}│┴"[j]
                index = i * 2 + j // 2
                if j % 2 == 0:
                    lines[j] += "─" * (just + 2)
                elif index < len(info):
                    lines[j] += f" {info[index]}{' ' * (just - alen(info[index]) + 1)}"
                else:
                    lines[j] += " " * (just + 2)
        return "\n".join(line + f"┐│{'┤' if info else '│'}│┘"[i] for i, line in enumerate(lines))


@makeImmutable
class Values:
    """Class for containing coordinate values for a given axis
    """

    def __init__(self, axis: Axis, vertices: tuple, multiplier: int = 1) -> None:
        """Initializing Values instance

        Multiplier is needed due to the fact that monospaced fonts used in consoles have a size ratio of 1:2.
        Using a multiplier makes sure that same-size shapes, like squares and circles do not look overtly stretched.

        Args:
            axis (Axis): Axis that these values belong to
            vertices (tuple): Transformed vertex positions
            multiplier (int, optional): Offset size multiplier. Defaults to 1.
        """
        ## Axis values, ordered by axis direction
        self.values = tuple(sorted(set(map(axis, vertices)), reverse=not axis))
        ## Absolute values of axis value differences
        self.differences = tuple(map(lambda pair: abs(pair[0] - pair[1]), zip(self.values, self.values[1:])))
        ## Minimal axis value increment
        self.minimum = min(self.differences) if self.differences else sys.maxsize
        if self.minimum < 0.001:
            raise ValueError("Mesh most likely contains floating point errors")
        ## Value offset multiplier
        self.multiplier = multiplier


@makeImmutable
class Labels:
    """Class for containing labels for axis values

    While Values is meant for calculating values, Labels is meant for printing them out
    """

    def __init__(self, values: Values, scale: float) -> None:
        """Initializing Labels instance

        Args:
            values (Values): Axis values
            scale (float): Axis scale
        """
        ## Rounded axis values to be used as labels in the final render
        self.labels = tuple(map(lambda value: str(round(value, 3)), values.values))
        ## Maximal label length
        self.just = max(map(len, self.labels))
        ## Multiplied character-sized column/row offsets
        self.offsets = (0,) + tuple(map(lambda d: round(d / scale) * values.multiplier - 1, values.differences))

    def __iter__(self):
        """Yielding offsets and labels
        """
        yield from zip(self.offsets, self.labels)

    def __len__(self) -> int:
        """Getting the number of o labels

        Returns:
            int: Number of labels
        """
        return len(self.labels)


@makeImmutable
## \todo Refactor
class Render:
    """Class for rendering 3D object(s) as a 2D view
    """

    def __init__(self, grid: Grid) -> None:
        """Initialising a Render instance

        Args:
            grid (Grid): Object with render settings
        """
        ## Render settings
        self.grid = grid

    def __call__(self, obj: Object, depth: int = 0) -> tuple:
        """Getting transformed mesh data of a specified object (recursively)

        Args:
            obj (Object): Object whose mesh is being transformed
            depth (int, optional): Current recursion depth. Defaults to 0.

        Returns:
            tuple: Tuples of transformed mesh data (vertices, edges)
        """
        vertices = tuple(set(vertex for face in obj.faces for vertex in face.points))
        edges = tuple(set(line for face in obj.faces for line in face))
        if depth < self.grid.depth:
            for child in obj.objects:
                vertices, edges = (a+b for a, b in zip((vertices, edges), self(child, depth + 1)))
        return tuple(map(obj.__matmul__, vertices)), tuple(map(obj.__matmul__, edges))

    def __str__(self) -> str:
        """Getting the text representation of a grid render

        Returns:
            str: ANSI colored string of the grid render
        """
        vertices, edges = self(self.grid.obj)
        vv = Values(self.grid.direction.vertical, vertices)
        hh = Values(self.grid.direction.horizontal, vertices, 2)
        vertical = Labels(vv, self.grid.scale(vv.minimum, hh.minimum))
        horizontal = Labels(hh, self.grid.scale(hh.minimum, vv.minimum))
        output = ""
        # Header
        for i in range(horizontal.just):
            output += " " * (vertical.just + 1)
            for offset, label in horizontal:
                output += f"{' ' * offset}{label.rjust(horizontal.just)[i]}"
            output += "\n"
        # Body
        for i, label in enumerate(vertical.labels):
            for j in range(vertical.offsets[i]):
                output += " " * (vertical.just + 1)
                for k in range(len(horizontal)):
                    output += f"{' ' * horizontal.offsets[k]}|"
                output += "\n"
            output += f"{label.rjust(vertical.just)} "
            for j in range(len(horizontal)):
                output += f"{'-' * horizontal.offsets[j]}+"
            output += f" {label}\n"
        # Footer
        for i in range(horizontal.just):
            if i > 0:
                output += "\n"
            output += " " * (vertical.just + 1)
            for offset, label in horizontal:
                output += f"{' ' * offset}{label.ljust(horizontal.just)[i]}"
        return output