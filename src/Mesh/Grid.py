## \file
# Functionality for rendering Object structure in console
from Utils.Decorators import makeImmutable
from Utils.Colors import NONE, AXIS, TEMPERATURE, lenANSI
from Math.Vector import V3
import math, re



@makeImmutable
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
        self.reverse = name.startswith("-")
        ## Axis values
        self.values = sorted(set(getattr(vertex, self.name) for vertex in vertices))
        ## Differences in axis values
        self.diffs = [self.values[i] - self.values[i-1] for i in range(1, len(self.values))]
        if self.reverse:
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



@makeImmutable
class View:
    """Class for rendering 3D objects as 2D views in console
    """

    def __init__(self, obj: "Object", vertices: set, vertical: str, horizontal: str, title: str) -> None:
        """Initialising a View instance

        Args:
            obj (Object): Object instance to render in console
            vertices (set): Subset of the object's vertices
            vertical (Axis): Vertical axis name
            horizontal (Axis): Horizontal axis name
            title (str): View title
        """
        ## Object to render
        self.obj = obj
        ## Subset of object's vertices to render
        self.vertices = vertices
        ## Vertical axis
        self.vertical = Axis(vertical, vertices)
        ## Horizontal axis
        self.horizontal = Axis(horizontal, vertices)
        ## View title
        self.title = title

    def _axisInfo(self) -> tuple:
        """Getting out a diagram of axis orientation

        Returns:
            tuple: 3 row strings representing selected axis
        """
        first = (" ", f"{AXIS[self.vertical.name]}{self.vertical.name.upper()}{NONE}", "     ")
        second = (" ", "┃", "     ")
        third = (f"╺{'━━╋'[::(-1,1)[self.horizontal.reverse]]}╸", f"{AXIS[self.horizontal.name]}{self.horizontal.name.upper()}{NONE}", " ")
        rows = tuple(map(lambda row: "".join(row[::(1,-1)[self.horizontal.reverse]]), (first, second, third)))
        return rows[::(-1,1)[self.vertical.reverse]]

    def _colorLegend(self) -> tuple:
        """Getting a legend for vertex colors

        Returns:
            tuple: Colors for vertex counts as a string in a tuple
        """
        return (" ".join(TEMPERATURE[i] + str(i) for i in range(len(TEMPERATURE))) + "+" + NONE, )
    
    def _printLegend(self) -> None:
        """Printing out grid legend
        """
        # Variables
        axis = self._axisInfo()
        info = (self.obj.name, f"{len(self.vertices)} vertices", self.title, ) + self._colorLegend()
        rows = (len(axis) + 1) // 2
        cols = math.ceil(len(info) / rows)
        lengths = [max(map(lenANSI, info[i * rows:(i+1) * rows])) for i in range(cols)]
        # Printing out top border
        print(f"╭{'─' * lenANSI(axis[0])}", end="")
        for c in range(cols):
            print(f"┬{'─' * (lengths[c] + 2)}", end="")
        print("╮")
        # Printing out rows
        for r, line in enumerate(axis):
            print(f"│{line}", end="")
            if r % 2 == 0:
                for c in range(cols):
                    index = c*rows+r//2
                    if len(info) > index:
                        print(f"│ {info[index]+' '*(lengths[c]-lenANSI(info[index]))} ", end="")
                    else:
                        print(f"│ {' '*lengths[c]} ", end="")
                print("│")
            else:
                for c in range(cols):
                    print(f"{'┼' if c else '├'}{'─' * (lengths[c] + 2)}", end="")
                print("┤" if info else "│")
        # Printing out bottom border
        print(f"╰{'─' * lenANSI(axis[0])}", end="")
        for c in range(cols):
            print(f"┴{'─' * (lengths[c] + 2)}", end="")
        print("╯")
    
    def _printVertices(self) -> None:
        """Printing out grid header
        """
        # Header
        for i in range(self.horizontal.just):
            print(" " * (self.vertical.just + 1), end="")
            for j, h in enumerate(self.horizontal.labels):
                if j > 0:
                    print(" " * round(self.horizontal.diffs[j-1] / self.horizontal.min *2-1), end="")
                print(str(h).rjust(self.horizontal.just)[i], end="")
            print()
        # Body
        for i, v in enumerate(self.vertical.labels):
            if i > 0:
                for j in range(round(self.vertical.diffs[i-1] / self.vertical.min - 1)):
                    print(" " * (self.vertical.just + 1), end="")
                    for k, h in enumerate(self.horizontal.labels):
                        if k > 0:
                            print(" " * round(self.horizontal.diffs[k-1] / self.horizontal.min *2-1), end="")
                        print("│", end="")
                    print()
            print(str(v).rjust(self.vertical.just) + "╶", end="")
            for j, h in enumerate(self.horizontal.labels):
                if j > 0:
                    print("─" * round(self.horizontal.diffs[j-1] / self.horizontal.min *2-1), end="")
                #print(f"{self.pointColor(vertical, horizontal, vertical.values[i], horizontal.values[j])}┼{NONE}", end="")
                print(f"┼", end="")
            print(f"╴{v}")
        # Footer
        for i in range(self.horizontal.just):
            print(" " * (self.vertical.just + 1), end="")
            for j, h in enumerate(self.horizontal.labels):
                if j > 0:
                    print(" " * round(self.horizontal.diffs[j-1] / self.horizontal.min *2-1), end="")
                print(str(h).ljust(self.horizontal.just)[i], end="")
            print()
    
    def print(self) -> None:
        """Printing out the grid view
        """
        self._printLegend()
        self._printVertices()



@makeImmutable
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
        ## All vertex positions found within the object (including children)
        self.vertices = self._getVertices()
    
    def _getVertices(self) -> tuple:
        """Getting a layer-indexed tuple of sets of vertices

        Returns:
            tuple: Tuple of sets of vertices (one for each depth layer)
        """
        vertices = []
        queue = [(self.obj, 0)]
        while queue:
            obj, layer = queue.pop(0)
            if layer == len(vertices):
                vertices.append(set())
            for face in obj.faces:
                for vertex in face:
                    vertices[layer].add(vertex)
            for child in obj.objects:
                queue.append((child, layer + 1))
        return tuple(vertices)
    
    def _selectVertices(self, depth: int) -> set:
        """Selecting vertices up to a certain layer depth

        Args:
            depth (int): Maximum layer depth

        Returns:
            set: Set of vertices found wihin the specified depth
        """
        return set.union(*self.vertices[:depth + 1])
    
    def print(self, depth: int = 0) -> None:
        """Printing out a grid

        Args:
            depth (int, optional): Maximum layer index. Defaults to 0.
        """
        assert depth >= 0, "Max depth cannot be a negative number"
        selected = self._selectVertices(depth)
        View(self.obj, selected, "-x", "-y", "TOP VIEW").print()
        View(self.obj, selected, "-z", "-y", "SIDE VIEW").print()
        View(self.obj, selected, "-z", "x", "FRONT VIEW").print()