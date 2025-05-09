## \file
# Functionality for rendering Object structure in console
# \todo Refactor and add tests
from . import Decorators, Colors, Mesh, Vector, Helpers
import enum


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

    def __init__(self, value: int) -> None:
        """Initialising an Axis instance
        """
        ## Line representing axis direction
        self.line = Mesh.Line(Vector.V3.ZERO, Vector.V3(**{str(self): value}))

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


class Show(enum.Enum):
    """Enums for adjusting vertex and line colors
    """

    ## Colorizing vertices based on their counts and disregarding line counts
    VERTICES = (lambda vertex, top, right, bottom, left: vertex, lambda line: 0)
    ## Colorizing vertices based on neighbouring line counts
    EDGES = (lambda vertex, top, right, bottom, left: max(top, right, bottom, left), lambda line: line)

    def __init__(self, point, line) -> None:
        """Initialising a Show instance

        Args:
            point: Function for updating color index for points
            line: Function for updating color index for lines
        """
        ## Function for adjusting point count
        self.point = point
        ## Function for adjusting line count
        self.line = line


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
            "faces": len(obj.faces),
            "triangles": sum(len(face.points) - 2 for face in obj.faces),
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
        yield f"{self.grid.direction.title} of {self.grid.show.name}"
        yield " ".join(f"{Colors.temperature(i)}{i}" for i in range(len(Colors.TEMPERATURE))) + "+" + Colors.NONE

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


class Values:
    """Class for containing detailed information on axis values
    """

    def __init__(self, axis: Axis, vertices: tuple, multiplier: int) -> None:
        """Initialising Values instance

        Args:
            axis (Axis): Axis
            vertices (tuple): Tuple of transformed vertex positions
            multiplier (int): Offset size multiplier
        """
        ## Axis
        self.axis = axis
        ## Axis values
        if not vertices:
            raise ValueError("No vertices were provided")
        self.values = sorted(set(map(axis, vertices)), reverse=not axis)
        ## Axis value labels
        self.labels = tuple(map(lambda value: str(round(value, 3)), self.values))
        ## Label justify length
        self.just = max(map(lambda value: len(str(value)), self.labels))
        differences = tuple(map(lambda pair: abs(pair[0] - pair[1]), zip(self.values, self.values[1:])))
        if differences:
            minimum = min(differences)
            if minimum < 0.001:
                raise ValueError("Mesh contains floating point errors")
            ## Axis value offsets
            self.offsets = tuple(map(lambda d: round(d / minimum) * multiplier - 1, differences))


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
        self.horizontal = Values(self.grid.direction.horizontal, self.data["vertices"], 2)
        ## Vertical axis values
        self.vertical = Values(self.grid.direction.vertical, self.data["vertices"], 1)
        ## Matrix of vertex counts
        self.vertexCounts = self.countVertices()
        ## Vertical and horizontal line counts
        self.verticalCounts, self.horizontalCounts = self.countLines()

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
        left = 0 if horizontal == 0 else self.horizontalCounts[vertical][horizontal - 1]
        top = 0 if vertical == 0 else self.verticalCounts[vertical - 1][horizontal]
        right = 0 if horizontal >= len(self.horizontal.values) - 1 else self.horizontalCounts[vertical][horizontal]
        bottom = 0 if vertical >= len(self.vertical.values) - 1 else self.verticalCounts[vertical][horizontal]
        count = self.grid.show.point(vertices, top, right, bottom, left)
        return f"{Colors.temperature(count)}{self.pointChar(vertical, horizontal)}{Colors.NONE}"

    def colorizeHorizontal(self, vertical: int, horizontal: int) -> str:
        """Colorizing a horizontal line based on the number of edges behind it

        Args:
            vertical (int): Vertical line value index
            horizontal (int): Horizontal line value index

        Returns:
            str: ANSI colored string representing the line
        """
        count = self.horizontalCounts[vertical][horizontal]
        chars = self.horizontal.offsets[horizontal]
        return f"{Colors.temperature(self.grid.show.line(count))}{('━' if count else '╌') * chars}{Colors.NONE}"

    def colorizeVertical(self, vertical: int, horizontal: int) -> str:
        """Colorizing a vertical line based on the number of edges behind it

        Args:
            vertical (int): Vertical line value index
            horizontal (int): Horizontal line value index

        Returns:
            str: ANSI colored character representing the line
        """
        count = self.verticalCounts[vertical][horizontal]
        return f"{Colors.temperature(self.grid.show.line(count))}{'┃' if count else '┆'}{Colors.NONE}"

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

    def countVertices(self) -> list:
        """Counting vertices whose values match axis values

        Returns:
            list: 2D list of vertex counts
        """
        counts = [[0 for _ in self.horizontal.values] for _ in self.vertical.values]
        for vertex in self.data["vertices"]:
            counts[self.vertical.values.index(self.vertical.axis(vertex))] \
                [self.horizontal.values.index(self.horizontal.axis(vertex))] += 1
        return counts

    def flattenLines(self, lines: set):
        """Flattening lines (removing their third dimension)

        Args:
            lines (set): Subset of the object's lines
        """
        for line in lines:
            try:
                yield line(**{({"x", "y", "z"} - {str(self.horizontal.axis), str(self.vertical.axis)}).pop(): 0})
            except ValueError:
                pass

    # noinspection DuplicatedCode
    def countLines(self) -> tuple:
        """Counting the number of lines for each axis value pair

        Returns:
            tuple: Tuple of 2D lists of line counts
        """
        verticalCounts = [[0 for _ in self.horizontal.values] for _ in range(len(self.vertical.values) - 1)]
        horizontalCounts = [[0 for _ in range(len(self.horizontal.values) - 1)] for _ in self.vertical.values]
        for line in self.flattenLines(self.data["edges"]):
            if line | self.vertical.axis.line:
                v1 = self.vertical.values.index(self.vertical.axis(line.a))
                v2 = self.vertical.values.index(self.vertical.axis(line.b))
                h = self.horizontal.values.index(self.horizontal.axis(line.a))
                for i in range(min(v1, v2), max(v1, v2)):
                    verticalCounts[i][h] += 1
            elif line | self.horizontal.axis.line:
                v = self.vertical.values.index(self.vertical.axis(line.a))
                h1 = self.horizontal.values.index(self.horizontal.axis(line.a))
                h2 = self.horizontal.values.index(self.horizontal.axis(line.b))
                for i in range(min(h1, h2), max(h1, h2)):
                    horizontalCounts[v][i] += 1
        return verticalCounts, horizontalCounts

    def __str__(self) -> str:
        """Getting string representation of the grid mesh

        Returns:
            str: ANSI colored string representing the grid view
        """
        output = ""
        # Header
        for i in range(self.horizontal.just):
            output += " " * (self.vertical.just + 1)
            for j, h in enumerate(self.horizontal.labels):
                if j > 0:
                    output += " " * self.horizontal.offsets[j - 1]
                output += str(h).rjust(self.horizontal.just)[i]
            output += "\n"
        # Body
        for i, v in enumerate(self.vertical.labels):
            if i > 0:
                for j in range(self.vertical.offsets[i - 1]):
                    output += " " * (self.vertical.just + 1)
                    for k, h in enumerate(self.horizontal.labels):
                        if k > 0:
                            output += " " * self.horizontal.offsets[k - 1]
                        output += self.colorizeVertical(i - 1, k)
                    output += "\n"
            output += str(v).rjust(self.vertical.just) + " "
            for j, h in enumerate(self.horizontal.labels):
                if j > 0:
                    output += self.colorizeHorizontal(i, j - 1)
                output += self.colorizePoint(i, j)
            output += f" {v}\n"
        # Footer
        for i in range(self.horizontal.just):
            output += " " * (self.vertical.just + 1)
            for j, h in enumerate(self.horizontal.labels):
                if j > 0:
                    output += " " * self.horizontal.offsets[j - 1]
                output += str(h).ljust(self.horizontal.just)[i]
            output += "\n"
        return output


# noinspection PyUnresolvedReferences
## \todo Add an option to show bounding boxes of objects
# \todo Add an option for toggling between fixed/independent axis value diffs
@Decorators.makeImmutable
class Grid:
    """Class for rendering 3D object(s) from a specified direction
    """

    def __init__(self, obj: Mesh.Object, depth: int = 0, direction: Direction = Direction.TOP, show: Show = Show.EDGES) -> None:
        """Initialising a Grid instance

        Args:
            obj (Mesh.Object): Object whose mesh will be rendered
            depth (int, optional): Depth from which mesh data will be gathered. Defaults to 0.
            direction (Direction, optional): Direction from which the object is viewed. Defaults to Direction.TOP.
            show (Show, optional): Selection of how colors do get shown. Defaults to Show.EDGES.
        """
        ## Object to visualise
        self.obj = obj
        ## Render depth
        self.depth = depth
        ## View direction
        self.direction = direction
        ## Show settings
        self.show = show

    def __str__(self) -> str:
        """Getting string representation of the grid

        Returns:
             str: String representation of the grid
        """
        return f"{Header(self)}\n{View(self)}"

    @staticmethod
    def all(*args, **kwargs) -> str:
        """Getting the render of an object from ALL directions

        Returns:
            str: String with all object renders
        """
        return "\n".join(str(Grid(*args, direction=direction, **kwargs)) for direction in Direction)