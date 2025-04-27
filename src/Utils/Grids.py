## \file
# Functionality for rendering Object structure in console
from . import Decorators, Colors, Mesh, Vector
import math, re, enum


class Point(enum.IntFlag):
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


class Show(enum.Enum):
    """Enum for the type of information View is supposed to show
    """

    ## Highlight vertices based on their count
    VERTICES = 0
    ## Highlight lines based on their count
    EDGES = 1

    @staticmethod
    def clamp(count: int) -> int:
        """Clamping the vertex/edge count to not overflow the color count

        Args:
            count (int): Number of vertices/edges to clamp

        Returns:
            int: Clamped final count corresponding to a specific color
        """
        if count >= len(Colors.TEMPERATURE):
            return len(Colors.TEMPERATURE) - 1
        return count

    def edge(self, edges: int) -> int:
        """Updating an edge count based on chosen show type

        Args:
            edges (int): Calculated edge count

        Returns:
            int: Clamped edge count
        """
        if self == Show.VERTICES:
            return 0
        if self == Show.EDGES:
            return Show.clamp(edges)
        raise NotImplementedError("Unexpected Show type")

    def vertex(self, vertices: int, edges: int) -> int:
        """Updating a vertex count based on chosen show type

        Args:
            vertices (int): Calculated vertex count
            edges (int): Maximum count of neighbouring edges

        Returns:
            int: Clamped vertex count
        """
        if self == Show.VERTICES:
            return Show.clamp(vertices)
        if self == Show.EDGES:
            return Show.clamp(edges)
        raise NotImplementedError("Unexpected Show type")


@Decorators.makeImmutable
class Axis:
    """Class for containing axis information
    """

    def __init__(self, name: str, vertices: set) -> None:
        """Initialising an Axis instance

        Args:
            name (str): Axis name
            vertices (set): Set of object vertices
        """
        ## Axis name
        assert re.fullmatch("-?[xyz]", name), "Invalid axis name"
        self.name = name[-1]
        ## Is the axis in reverse?
        self.reversed = name.startswith("-")
        ## Axis values
        self.values = sorted(set(getattr(vertex, self.name) for vertex in vertices))
        assert len(self.values), "Axis has to contain at least one vertex value"
        ## Differences in axis values
        differences = [self.values[i] - self.values[i - 1] for i in range(1, len(self.values))]
        if self.reversed:
            self.values.reverse()
            differences.reverse()
        if differences:
            minimum = min(differences)
            assert minimum > 0.001, "Map contains floating point errors"
            ## Axis value distances
            self.distances = tuple(map(lambda d: round(d / minimum), differences))
        else:
            self.distances = tuple()
        ## Axis value labels
        self.labels = tuple(map(lambda value: str(round(value, 3)), self.values))
        ## Most amount of space a single axis value can take up
        self.just = max(map(lambda value: len(str(value)), self.labels))

    def match(self, vertex: Vector.V3, value: float) -> bool:
        """Checking whether an axis value "matches" a vertex point

        Args:
            vertex (Vector.V3): Vertex to check
            value (float): Value on the current axis

        Returns:
            func: True if the vertex has the value as a component of the current axis
        """
        return getattr(vertex, self.name) == value


# noinspection PyUnresolvedReferences
## \todo Make line count calculations much faster
# \todo Update legend information and add proper vertex and line counts according to Blender
@Decorators.makeImmutable
class View:
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

    def _axisInfo(self) -> tuple:
        """Getting out a diagram of axis orientation

        Returns:
            tuple: 3 row strings representing selected axis
        """
        first = (" ", f"{Colors.AXIS[self.vertical.name]}{self.vertical.name.upper()}{Colors.NONE}", "     ")
        second = (" ", "┃", "     ")
        third = (f"╺{'━━╋'[::(-1, 1)[self.horizontal.reversed]]}╸",
                 f"{Colors.AXIS[self.horizontal.name]}{self.horizontal.name.upper()}{Colors.NONE}", " ")
        rows = tuple(map(lambda row: "".join(row[::(1, -1)[self.horizontal.reversed]]), (first, second, third)))
        return rows[::(-1, 1)[self.vertical.reversed]]

    @staticmethod
    def _colorLegend() -> tuple:
        """Getting a legend for vertex colors

        Returns:
            tuple: Colors for vertex counts as a string in a tuple
        """
        return (" ".join(f"{Colors.TEMPERATURE[i]}{i}" for i in range(len(Colors.TEMPERATURE))) + "+" + Colors.NONE,)

    def _printLegend(self) -> None:
        """Printing out grid legend
        """
        # Variables
        axis = self._axisInfo()
        info = (
                   f"{Colors.BOLD}{sum(sum(row) for row in self.vertexCounts)}{Colors.NONE} vertices",
                   self.title
               ) + self._colorLegend()
        rows = (len(axis) + 1) // 2
        cols = math.ceil(len(info) / rows)
        lengths = [max(map(Colors.lenANSI, info[i * rows:(i + 1) * rows])) for i in range(cols)]
        # Printing out top border
        print(f"╭{'─' * Colors.lenANSI(axis[0])}", end="")
        for c in range(cols):
            print(f"┬{'─' * (lengths[c] + 2)}", end="")
        print("╮")
        # Printing out rows
        for r, line in enumerate(axis):
            print(f"│{line}", end="")
            if r % 2 == 0:
                for c in range(cols):
                    index = c * rows + r // 2
                    if len(info) > index:
                        print(f"│ {info[index] + ' ' * (lengths[c] - Colors.lenANSI(info[index]))} ", end="")
                    else:
                        print(f"│ {' ' * lengths[c]} ", end="")
                print("│")
            else:
                for c in range(cols):
                    print(f"{'┼' if c else '├'}{'─' * (lengths[c] + 2)}", end="")
                print("┤" if info else "│")
        # Printing out bottom border
        print(f"╰{'─' * Colors.lenANSI(axis[0])}", end="")
        for c in range(cols):
            print(f"┴{'─' * (lengths[c] + 2)}", end="")
        print("╯")

    def pointChar(self, vertical: int, horizontal: int) -> str:
        """Getting a character representing point shape

        Args:
            vertical (int): Vertical vertex index
            horizontal (int): Horizontal vertex index

        Returns:
            str: Character representing point shape
        """
        point = Point.NONE
        if horizontal > 0 and self.horizontalCounts[vertical][horizontal - 1]:
            point |= Point.LEFT
        if vertical > 0 and self.verticalCounts[vertical - 1][horizontal]:
            point |= Point.TOP
        if horizontal < len(self.horizontal.values) - 1 and self.horizontalCounts[vertical][horizontal]:
            point |= Point.RIGHT
        if vertical < len(self.vertical.values) - 1 and self.verticalCounts[vertical][horizontal]:
            point |= Point.BOTTOM
        return str(point)

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


# noinspection PyUnresolvedReferences
@Decorators.makeImmutable
class Grid:
    """Class for processing requests for the rendering of 3D objects in console
    """

    def __init__(self, obj: "Object") -> None:
        """Initialising a Grid instance

        Args:
            obj (Object): Object to create print grids of
        """
        ## Object to visualise
        self.obj = obj

    def _transformedFaces(self, obj: "Object", depth: int) -> set:
        """Getting all faces found up to the specified depth, transformed

        Args:
            obj (Object): Object whose faces are being gathered
            depth (int): Remaining layer depth to go down to

        Returns:
            set: Object faces with transformed vertex positions
        """
        faces = set(obj.faces)
        if depth > 0:
            for child in obj.objects:
                faces = faces.union(self._transformedFaces(child, depth - 1))
        return set(map(obj.transform, faces))

    def print(self, depth: int = 0) -> None:
        """Printing out a grid

        Args:
            depth (int, optional): Maximum layer index. Defaults to 0.
        """
        assert depth >= 0, "Max depth cannot be a negative number"
        faces = self._transformedFaces(self.obj, depth)
        View(faces, "-x", "-y", "TOP VIEW").print()
        View(faces, "-z", "-y", "FRONT VIEW").print()
        View(faces, "-z", "x", "SIDE VIEW").print()