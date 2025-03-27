## \file
# Functionality for rendering Object structure in console
from Utils.Decorators import makeImmutable
from Math.Vector import V3
import math



@makeImmutable
class Axis:
    """Class for containing axis information
    """

    def __init__(self, vertices: set, name: str, reverse: bool = False) -> None:
        """Initialising an Axis instance

        Args:
            vertices (set): Set of vertex positions (relative to parent's origin)
            name (str): Axis name ("x"/"y"/"z")
            reverse (bool, optional): Should the axis values be reversed? Defaults to False.
        """
        ## Axis name
        self.name = name
        ## Is the axis in reverse?
        self.reverse = reverse
        ## Axis values
        self.values = sorted(set(getattr(vertex, name) for vertex in vertices))
        ## Differences in axis values
        self.diffs = [self.values[i] - self.values[i-1] for i in range(1, len(self.values))]
        if reverse:
            self.values.reverse()
            self.diffs.reverse()
        ## Axis value labels
        self.labels = tuple(map(lambda value: str(round(value, 3)), self.values))
        ## Minimum axis value difference
        if self.diffs:
            self.min = min(self.diffs)
            assert self.min > 0, "Minimal difference has to be positive"
        else:
            self.min = 0
        ## Most amount of space a single axis value can take up
        self.just = max(map(lambda value: len(str(value)), self.labels))
    
    def match(self, vertex: V3, value: float) -> bool:
        """Checking whether an axis value "matches" a vertex point

        Args:
            vertex (V3): Vertex to check
            value (float): Value on the current axis

        Returns:
            func: True if the vertex has the value as a component of the current axis
        """
        return getattr(vertex, self.name) == value


## Grid colors, from coldest to hottest
GRID_COLORS = ("\033[97m", "\033[94;1m", "\033[96;1m", "\033[92;1m", "\033[93;1m", "\033[91;1m", "\033[95;1m")

## "Reset" color
NO_COLOR = "\033[0m"

## Colors for axis names
AXIS_COLORS = {"x": "\033[91;1m", "y": "\033[92;1m", "z": "\033[94;1m"}
    
def lenANSI(string: str) -> int:
    """Getting the length of a string while ignoring ANSI escape sequences

    Args:
        string (str): String to get the length of

    Returns:
        int: Length of the pure string
    """
    for color in GRID_COLORS + tuple(AXIS_COLORS.values()) + (NO_COLOR,):
        string = string.replace(color, "")
    return len(string)


## \todo Add functionality for generating grid recursively (the whole hierarchy, not just one object)
class Grid:
    """Functionality for rendering Object vertices in console from multiple perspectives

    Requires a subclass to have a "faces" property (a list of lists of V3 vertices)
    """

    def axisLegend(self, V: Axis, H: Axis) -> tuple:
        """Getting axis information for the grid legend

        Args:
            V (Axis): Vertical axis
            H (Axis): Horizontal axis

        Returns:
            tuple: 3 row strings representing selected axis
        """
        first = (" ", f"{AXIS_COLORS[V.name]}{V.name.upper()}{NO_COLOR}", "     ")
        second = (" ", "┃", "     ")
        third = (f"╺{'━━╋' if H.reverse else '╋━━'}╸", f"{AXIS_COLORS[H.name]}{H.name.upper()}{NO_COLOR}", " ")
        rows = tuple(map(lambda row: "".join(row[::-1 if H.reverse else 1]), (first, second, third)))
        return rows[::1 if V.reverse else -1]

    def colorLegend(self) -> str:
        """Getting a legend for vertex colors

        Returns:
            str: Colors for vertex counts
        """
        return " ".join(GRID_COLORS[i] + str(i) for i in range(len(GRID_COLORS))) + "+" + NO_COLOR
    
    def printGridLegend(self, V: Axis, H: Axis) -> None:
        """Printing out grid axis legend

        Args:
            V (Axis): Vertical axis
            H (Axis): Horizontal axis
        """
        axis = self.axisLegend(V, H)
        info = (self.colorLegend(), )
        rows = (len(axis) + 1) // 2
        cols = math.ceil(len(info) / rows)
        lengths = [max(map(lenANSI, info[i * rows:(i+1) * rows])) for i in range(cols)]
        print(f"╭{'─' * lenANSI(axis[0])}", end="")
        for c in range(cols):
            print(f"┬{'─' * (lengths[c] + 2)}", end="")
        print("╮")
        for r, line in enumerate(axis):
            print(f"│{line}", end="")
            if r % 2 == 0:
                for c in range(cols):
                    index = c*rows+r//2
                    print(f"│ {info[index].ljust(lengths[c]) if len(info) > index else ' '*lengths[c]} ", end="")
                print("│")
            else:
                for c in range(cols):
                    print(f"{'┼' if c else '├'}{'─' * (lengths[c] + 2)}", end="")
                print("┤" if info else "│")
        print(f"╰{'─' * lenANSI(axis[0])}", end="")
        for c in range(cols):
            print(f"┴{'─' * (lengths[c] + 2)}", end="")
        print("╯")
    
    def getVertices(self, depth: int = 0) -> set:
        """Getting a set of vertices present in the current hierarchy.

        Args:
            depth (int, optional): Remaining recursion depth. Defaults to 0.

        Returns:
            list: Set of vertices in the current hierarchy (relative to parent's origin)
        """
        vertices = set(vertex for face in self.faces for vertex in face)
        if depth > 0:
            for child in self.objects:
                vertices = vertices.union(child.getVertices(depth - 1))
        return set(map(lambda v: v + self.bounds.O, vertices))
    
    def pointColor(self, V: Axis, H: Axis, VV: float, HV: float) -> str:
        """Getting a color of a single point

        Args:
            V (Axis): Vertical axis
            H (Axis): Horizontal axis
            VV (float): Vertical axis value
            HV (float): Horizontal axis value

        Returns:
            str: ANSI color representing the point
        """
        vertices = set()
        for face in self.faces:
            for vertex in face:
                if V.match(vertex, VV) and H.match(vertex, HV):
                    vertices.add(vertex)
        count = len(vertices)
        if count > len(GRID_COLORS):
            count = len(GRID_COLORS) - 1
        return GRID_COLORS[count]
    
    def gridHeader(self, V: Axis, H: Axis) -> None:
        """Printing out grid header

        Args:
            V (Axis): Vertical axis
            H (Axis): Horizontal axis
        """
        for i in range(H.just):
            print(" " * (V.just + 1), end="")
            for j, h in enumerate(H.labels):
                if j > 0:
                    print(" " * round(H.diffs[j-1] / H.min *2-1), end="")
                print(str(h).rjust(H.just)[i], end="")
            print()
    
    def gridBody(self, V: Axis, H: Axis) -> None:
        """Printing out grid body

        Args:
            V (Axis): Vertical axis
            H (Axis): Horizontal axis
        """
        for i, v in enumerate(V.labels):
            if i > 0:
                for j in range(round(V.diffs[i-1] / V.min - 1)):
                    print(" " * (V.just + 1), end="")
                    for k, h in enumerate(H.labels):
                        if k > 0:
                            print(" " * round(H.diffs[k-1] / H.min *2-1), end="")
                        print("┃", end="")
                    print()
            print(str(v).rjust(V.just) + f"{self.pointColor(V, H, V.values[i], H.values[0])}╺{NO_COLOR}", end="")
            for j, h in enumerate(H.labels):
                if j > 0:
                    print("━" * round(H.diffs[j-1] / H.min *2-1), end="")
                print(f"{self.pointColor(V, H, V.values[i], H.values[j])}╋{NO_COLOR}", end="")
            print(f"{self.pointColor(V, H, V.values[i], H.values[-1])}╸{NO_COLOR}" + str(v))
    
    def gridFooter(self, V: Axis, H: Axis) -> None:
        """Printing out grid footer

        Args:
            V (Axis): Vertical axis
            H (Axis): Horizontal axis
        """
        for i in range(H.just):
            print(" " * (V.just + 1), end="")
            for j, h in enumerate(H.labels):
                if j > 0:
                    print(" " * round(H.diffs[j-1] / H.min *2-1), end="")
                print(str(h).ljust(H.just)[i], end="")
            print()

    def printGrid(self, V: Axis, H: Axis) -> None:
        """Printing out a grid

        Args:
            V (Axis): Vertical axis
            H (Axis): Horizontal axis
        """
        self.printGridLegend(V, H)
        for method in (self.gridHeader, self.gridBody, self.gridFooter):
            method(V, H)
    
    def printGrids(self, depth: int = 0) -> None:
        """Printing out a string representations of an object in a grid view

        Args:
            depth (int, optional): Remaining recursion depth. Defaults to 0.
        """
        if not self.faces:
            return
        vertices = self.getVertices(depth)
        self.printGrid(Axis(vertices, "x", True), Axis(vertices, "y", True))
        self.printGrid(Axis(vertices, "z", True), Axis(vertices, "y", True))
        self.printGrid(Axis(vertices, "z", True), Axis(vertices, "x"))