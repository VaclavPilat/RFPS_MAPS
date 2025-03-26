## \file
# Functionality for rendering Object structure in console
from Utils.Decorators import makeImmutable
from Math.Vector import V3



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



## \todo Add functionality for generating grid recursively (the whole hierarchy, not just one object)
class Grid:
    """Functionality for rendering Object vertices in console from multiple perspectives

    Requires a subclass to have a "faces" property (a list of lists of V3 vertices)
    """

    ## Grid colors, from coldest to hottest
    GRID_COLORS = ("\033[37m", "\033[34m", "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[35m")

    ## "Reset" color
    NO_COLOR = "\033[0m"

    def gridLegend(self) -> None:
        """Printing out a legend for grid colors
        """
        print(" ".join(self.GRID_COLORS[i] + str(i) for i in range(len(self.GRID_COLORS))), end=f"+{self.NO_COLOR}\n")
    
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
        if count > len(self.GRID_COLORS):
            count = len(self.GRID_COLORS) - 1
        return self.GRID_COLORS[count]
    
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
            print(str(v).rjust(V.just) + f"{self.pointColor(V, H, V.values[i], H.values[0])}╺{self.NO_COLOR}", end="")
            for j, h in enumerate(H.labels):
                if j > 0:
                    print("━" * round(H.diffs[j-1] / H.min *2-1), end="")
                print(f"{self.pointColor(V, H, V.values[i], H.values[j])}╋{self.NO_COLOR}", end="")
            print(f"{self.pointColor(V, H, V.values[i], H.values[-1])}╸{self.NO_COLOR}" + str(v))
    
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
        self.gridLegend()
        self.printGrid(Axis(vertices, "x", True), Axis(vertices, "y", True))
        self.printGrid(Axis(vertices, "z", True), Axis(vertices, "y", True))
        self.printGrid(Axis(vertices, "z", True), Axis(vertices, "x"))