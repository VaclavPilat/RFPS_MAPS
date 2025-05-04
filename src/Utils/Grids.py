## \file
# Functionality for rendering Object structure in console
# \todo Refactor and add tests
from . import Decorators, Colors, Mesh, Vector, Helpers
import math, re, enum


class Shape(enum.IntFlag):
    """Flags for the shape of a vertex character shown in View
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
        """
        return "┼╹╺┗╻┃┏┣╸┛━┻┓┫┳╋"[self]


class Axis(enum.Enum):
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

    def __bool__(self) -> bool:
        """Checking whether the axis is positive or negative

        Returns:
            bool: True if the axis is positive
        """
        return self.value > 0

    def __neg__(self) -> "Axis":
        """Changing axis from positive to negative or vice versa

        Returns:
            Axis: Negated axis
        """
        return Axis(-self.value)

    def __str__(self) -> str:
        """Getting a character representing axis name

        Returns:
            str: Character representing axis name
        """
        return self.name[-1].lower()

    def __call__(self, vector: Vector.V3) -> float:
        """Getting the value of a vector that corresponds to self axis

        Args:
            vector (Vector.V3): Vector to get the axis value of

        Returns:
            float: Axis value
        """
        return getattr(vector, str(self))


class Direction(enum.Enum):
    """Enums representing the directions a 3D object can be rendered from
    """

    ## Top view direction
    TOP = ("TOP VIEW", -Axis.X, -Axis.Y)
    ## Front view direction
    FRONT = ("FRONT VIEW", -Axis.Z, -Axis.Y)
    ## Side view direction
    SIDE = ("SIDE VIEW", -Axis.Z, Axis.X)

    def __init__(self, title: str, vertical: Axis, horizontal: Axis) -> None:
        """Initializing a Direction instance

        Args:
            title (str): Direction title
            vertical (Axis): Vertical axis
            horizontal (Axis): Horizontal axis
        """
        ## Direction title
        self.title = title
        ## Vertical axis
        self.vertical = vertical
        ## Horizontal axis
        self.horizontal = horizontal

    def __iter__(self):
        """Getting strings representing the direction
        """
        top = (f"╺{'╋━━'[::1 if self.horizontal else -1]}╸",
               f"{Colors.AXIS[str(self.horizontal)]}{self.horizontal.name[-1]}{Colors.NONE}", " ")
        middle = (" ", "┃", "     ")
        bottom = (" ", f"{Colors.AXIS[str(self.vertical)]}{self.vertical.name[-1]}{Colors.NONE}", "     ")
        for line in (top, middle, bottom)[::1 if self.vertical else -1]:
            yield "".join(line[::1 if self.horizontal else -1])


# noinspection PyUnresolvedReferences
## \todo Make line count calculations much faster
# \todo Update legend information and add proper vertex and line counts according to Blender
@Decorators.makeImmutable
class _View:
    """Class for rendering 3D objects as 2D views in console
    """

    def __init__(self, faces: set, vertical: str, horizontal: str, title: str) -> None:
        """Initialising a View instance

        Args:
            faces (tuple): Object faces to render
            vertical (Axis): Vertical axis name
            horizontal (Axis): Horizontal axis name
            title (str): View title
        """
        lines = set(line for face in faces for line in face)
        vertices = set(line.a for line in lines)
        ## Vertical axis
        self.vertical = Axis(vertical, vertices)
        ## Horizontal axis
        self.horizontal = Axis(horizontal, vertices)
        ## View title
        self.title = title
        ## Matrix of vertex counts for all axis value intersections
        self.vertexCounts = self._countVertices(vertices)
        ## Matrices of horizontal and vertical line counts for all axis value pairs
        self.horizontalCounts, self.verticalCounts = self._countLines(lines)

    def _countVertices(self, vertices: set) -> tuple:
        """Counting then number of vertices for each axis value intersection

        Args:
            vertices (set): Subset of the object's vertices

        Returns:
            tuple: 2D tuple of vertex counts
        """
        return tuple(tuple(
            len(list(filter(
                lambda vertex: self.vertical.match(vertex, v) and self.horizontal.match(vertex, h),
                vertices
            ))) for h in self.horizontal.values) for v in self.vertical.values)

    def _countLines(self, lines: set) -> tuple:
        """Counting then number of lines for each axis value pair

        Args:
            lines (set): Subset of the object's lines

        Returns:
            tuple: 2D tuples of line counts, for horizontal and vertical lines
        """
        lines = tuple(self._flattenLines(lines))
        return (
            tuple(tuple(
                len(list(filter(
                    lambda line: Mesh.Line(
                        Vector.V3(**{self.horizontal.name: h1, self.vertical.name: v}),
                        Vector.V3(**{self.horizontal.name: h2, self.vertical.name: v})
                    ) in line,
                    lines
                ))) for h1, h2 in zip(self.horizontal.values, self.horizontal.values[1:])
            ) for v in self.vertical.values),
            tuple(tuple(
                len(list(filter(
                    lambda line: Mesh.Line(
                        Vector.V3(**{self.horizontal.name: h, self.vertical.name: v1}),
                        Vector.V3(**{self.horizontal.name: h, self.vertical.name: v2})
                    ) in line,
                    lines
                ))) for h in self.horizontal.values
            ) for v1, v2 in zip(self.vertical.values, self.vertical.values[1:]))
        )

    def _flattenLines(self, lines: set):
        """Flattening lines (removing their third dimension)

        Args:
            lines (set): Subset of the object's lines
        """
        for line in lines:
            try:
                yield line(**{({"x", "y", "z"} - {self.horizontal.name, self.vertical.name}).pop(): 0})
            except ValueError:
                pass

    def pointChar(self, vertical: int, horizontal: int) -> str:
        """Getting a character representing point shape

        Args:
            vertical (int): Vertical vertex index
            horizontal (int): Horizontal vertex index

        Returns:
            str: Character representing point shape
        """
        shape = Shape.NONE
        if horizontal > 0 and self.horizontalCounts[vertical][horizontal - 1]:
            shape |= Shape.LEFT
        if vertical > 0 and self.verticalCounts[vertical - 1][horizontal]:
            shape |= Shape.TOP
        if horizontal < len(self.horizontal.values) - 1 and self.horizontalCounts[vertical][horizontal]:
            shape |= Shape.RIGHT
        if vertical < len(self.vertical.values) - 1 and self.verticalCounts[vertical][horizontal]:
            shape |= Shape.BOTTOM
        return str(shape)

    def colorizePoint(self, vertical: int, horizontal: int) -> str:
        """Colorizing a single point based on the number of vertices behind it

        Args:
            vertical (int): Vertical axis value index
            horizontal (int): Horizontal axis value index

        Returns:
            str: ANSI colored box character representing the point
        """
        vertices = self.vertexCounts[vertical][horizontal]
        edges = max(
            0 if horizontal == 0 else self.horizontalCounts[vertical][horizontal - 1],
            0 if vertical == 0 else self.verticalCounts[vertical - 1][horizontal],
            0 if horizontal >= len(self.horizontal.values) - 1 else self.horizontalCounts[vertical][horizontal],
            0 if vertical >= len(self.vertical.values) - 1 else self.verticalCounts[vertical][horizontal]
        )
        return f"{Colors.TEMPERATURE[Show.VERTICES.vertex(vertices, edges)]}{self.pointChar(vertical, horizontal)}{Colors.NONE}"

    def colorizeHorizontal(self, vertical: int, horizontal: int) -> str:
        """Colorizing a horizontal line based on the number of edges behind it

        Args:
            vertical (int): Vertical line value index
            horizontal (int): Horizontal line value index

        Returns:
            str: ANSI colored string representing the line
        """
        count = self.horizontalCounts[vertical][horizontal]
        chars = self.horizontal.distances[horizontal] * 2 - 1
        return f"{Colors.TEMPERATURE[Show.VERTICES.edge(count)]}{('━' if count else '╌') * chars}{Colors.NONE}"

    def colorizeVertical(self, vertical: int, horizontal: int) -> str:
        """Colorizing a vertical line based on the number of edges behind it

        Args:
            vertical (int): Vertical line value index
            horizontal (int): Horizontal line value index

        Returns:
            str: ANSI colored character representing the line
        """
        count = self.verticalCounts[vertical][horizontal]
        return f"{Colors.TEMPERATURE[Show.VERTICES.edge(count)]}{'┃' if count else '┆'}{Colors.NONE}"

    def _printVertices(self) -> None:
        """Printing out grid header
        """
        # Header
        for i in range(self.horizontal.just):
            print(" " * (self.vertical.just + 1), end="")
            for j, h in enumerate(self.horizontal.labels):
                if j > 0:
                    print(" " * (self.horizontal.distances[j - 1] * 2 - 1), end="")
                print(str(h).rjust(self.horizontal.just)[i], end="")
            print()
        # Body
        for i, v in enumerate(self.vertical.labels):
            if i > 0:
                for j in range(self.vertical.distances[i - 1] - 1):
                    print(" " * (self.vertical.just + 1), end="")
                    for k, h in enumerate(self.horizontal.labels):
                        if k > 0:
                            print(" " * (self.horizontal.distances[k - 1] * 2 - 1), end="")
                        print(self.colorizeVertical(i - 1, k), end="")
                    print()
            print(str(v).rjust(self.vertical.just) + " ", end="")
            for j, h in enumerate(self.horizontal.labels):
                if j > 0:
                    print(self.colorizeHorizontal(i, j - 1), end="")
                print(self.colorizePoint(i, j), end="")
            print(f" {v}")
        # Footer
        for i in range(self.horizontal.just):
            print(" " * (self.vertical.just + 1), end="")
            for j, h in enumerate(self.horizontal.labels):
                if j > 0:
                    print(" " * (self.horizontal.distances[j - 1] * 2 - 1), end="")
                print(str(h).ljust(self.horizontal.just)[i], end="")
            print()

    def print(self) -> None:
        """Printing out the grid view
        """
        self._printLegend()
        self._printVertices()


class Header:
    """Class for displaying basic information about a grid
    """

    def __init__(self, grid: "Grid") -> None:
        """Initializing a Header instance

        Args:
            grid (Grid): Grid instance to describe
        """
        ## Source grid
        self.grid = grid
        ## Data counts
        self.counts = self.count(self.grid.obj, self.grid.depth)

    def count(self, obj: Mesh.Object, depth: int) -> dict:
        """Counting faces, edges and vertices of a specified object (recursively)

        Args:
            obj (Mesh.Object): Object whose mesh is being counted
            depth (int): Remaining recursion depth

        Returns:
            dict: Dictionary of Blender-like vertex, edge and face counts
        """
        counts = {
            "objects": 1,
            "vertices": len(set(vertex for face in obj.faces for vertex in face.points)),
            "edges": len(set(line for face in obj.faces for line in face)),
            "faces": len(obj.faces)
        }
        if depth > 0:
            for child in obj.objects:
                for key, value in self.count(child, depth - 1).items():
                    counts[key] += value
        return counts

    def __iter__(self):
        """Getting string information about the object being rendered to be displayed
        """
        # First column
        yield f"{Colors.BOLD}{self.grid.obj.name}{Colors.NONE}"
        yield ", ".join(f"{value} {key}" for key, value in self.counts.items())
        # Second column
        yield self.grid.direction.title
        yield " ".join(f"{Colors.TEMPERATURE[i]}{i}" for i in range(len(Colors.TEMPERATURE))) + "+" + Colors.NONE

    def __str__(self) -> str:
        """Getting a string representation of a grid header

        Returns:
             str: ANSI colored string representation of a grid header
        """
        info = tuple(self)
        lines = [f"╭{'─' * 7}", *(f"│{line}" for line in self.grid.direction), f"╰{'─' * 7}"]
        for i in range((len(info) + 1) // 2):
            just = max(map(Colors.alen, info[i * 2:i * 2 + 2]))
            for j in range(5):
                lines[j] += f"┬│{'┼' if i else '├'}│┴"[j]
                if j % 2 == 0:
                    lines[j] += "─" * (just + 2)
                elif i * 2 + j // 2 < len(info):
                    lines[j] += f" {info[i * 2 + j // 2]}{' ' * (just - Colors.alen(info[i * 2 + j // 2]) + 1)}"
                else:
                    lines[j] += " " * (just + 2)
        return "\n".join(line + f"╮│{'┤' if info else '│'}│╯"[i] for i, line in enumerate(lines))


## \note `distances = tuple(map(lambda d: round(d / minimum), differences))`
class Values:
    """Class for containing detailed information on axis values
    """

    def __init__(self, axis: Axis, vertices: tuple) -> None:
        """Initialising Values instance

        Args:
            axis (Axis): Axis
            vertices (tuple): Tuple of transformed vertex positions
        """
        ## Axis values
        if not vertices:
            raise ValueError("No vertices were provided")
        self.values = sorted(set(map(axis, vertices)), reverse=not axis)
        ## Axis value differences
        self.differences = tuple(map(lambda pair: abs(pair[0] - pair[1]), zip(self.values, self.values[1:])))
        if self.differences and min(self.differences) < 0.001:
            raise ValueError("Mesh contains floating point errors")
        ## Axis value labels
        self.labels = tuple(map(lambda value: str(round(value, 3)), self.values))
        ## Label justify length
        self.justify = max(map(lambda value: len(str(value)), self.labels))


class View:
    """Class for rendering a 3D mesh as text
    """

    def __init__(self, grid: "Grid") -> None:
        """Initializing a View instance

        Args:
            grid (Grid): Grid instance to visualise
        """
        ## Source grid
        self.grid = grid
        ## Transformed source data
        self.data = self.transform(self.grid.obj, self.grid.depth)
        ## Horizontal axis values
        self.horizontal = Values(self.grid.direction.horizontal, self.data["vertices"])
        ## Vertical axis values
        self.vertical = Values(self.grid.direction.vertical, self.data["vertices"])

    def transform(self, obj: Mesh.Object, depth: int) -> dict:
        """Getting transformed mesh data of a specified object (recursively)

        Args:
            obj (Mesh.Object): Object whose mesh is being transformed
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

    def __str__(self) -> str:
        """Getting string representation of the grid mesh

        Returns:
            str: ANSI colored string representing the grid view
        """
        return f"{len(self.data['vertices'])} vertices, {len(self.data['edges'])} edges"


# noinspection PyUnresolvedReferences
## \todo Add an option to show bounding boxes of objects
# \todo Add an option for toggling between fixed/independent axis value diffs
@Decorators.makeImmutable
class Grid:
    """Class for rendering 3D object(s) from a specified direction
    """

    def __init__(self, obj: Mesh.Object, direction: Direction, depth: int = 0) -> None:
        """Initialising a Grid instance

        Args:
            obj (Mesh.Object): Object whose mesh will be rendered
            direction (Direction): Direction from which the object is viewed
            depth (int, optional): Depth from which mesh data will be gathered. Defaults to 0.
        """
        ## Object to visualise
        self.obj = obj
        ## View direction
        self.direction = direction
        ## Render depth
        assert depth >= 0, "Depth cannot be negative"
        self.depth = depth

    def __str__(self) -> str:
        """Getting string representation of the grid

        Returns:
             str: String representation of the grid
        """
        return f"{Header(self)}\n{View(self)}"

    @staticmethod
    @Helpers.elapsedTime
    def all(*args, **kwargs) -> str:
        """Getting the render of an object from ALL directions

        Returns:
            str: String with all object renders
        """
        return "\n".join(str(Grid(*args, direction=direction, **kwargs)) for direction in Direction)