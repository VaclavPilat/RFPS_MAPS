## \file
# Functionality for rendering Object structure in console
from Utils.Decorators import makeImmutable



@makeImmutable
class Axis:
    """Class for containing axis information
    """

    def __init__(self, grid: "Grid", name: str, reverse: bool = False) -> None:
        """Initialising an Axis instance

        Args:
            grid (Grid): Grid object
            name (str): Axis name ("x" / "y"/ "z")
            reverse (bool, optional): Should the axis values be reversed? Defaults to False.
        """
        ## Axis name
        self.name = name
        ## Axis values
        self.values = sorted(set(getattr(vertex, name) for face in grid.faces for vertex in face))
        ## Differences in axis values
        self.diffs = [self.values[i] - self.values[i-1] for i in range(1, len(self.values))]
        if reverse:
            self.values.reverse()
            self.diffs.reverse()
        ## Axis value labels
        self.labels = tuple(map(lambda value: str(round(value, 3)), self.values))
        ## Minimum axis value difference
        self.min = min(self.diffs)
        assert self.min > 0, "Minimal difference has to be positive"
        ## Most amount of space a single axis value can take up
        self.just = max(map(lambda value: len(str(value)), self.labels))
    
    def match(self) -> "func":
        """Returns a function for checking whether a vertex point matches an axis value

        Returns:
            func: Matching function
        """
        return lambda vertex, value: getattr(vertex, self.name) == value



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
        print(" ".join(self.GRID_COLORS[i] + str(i) for i in range(len(self.GRID_COLORS))), end="+\033[0m\n")
    
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
        count = 0
        for face in self.faces:
            for vertex in face:
                if V.match()(vertex, VV) and H.match()(vertex, HV):
                    count += 1
                    break
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
                    print(" " * int(H.diffs[j-1] // H.min *2-1), end="")
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
                for j in range(int(V.diffs[i-1] // V.min) - 1):
                    print(" " * (V.just + 1), end="")
                    for k, h in enumerate(H.labels):
                        if k > 0:
                            print(" " * int(H.diffs[k-1] // H.min *2-1), end="")
                        print("┃", end="")
                    print()
            print(str(v).rjust(V.just) + "╺", end="")
            for j, h in enumerate(H.labels):
                if j > 0:
                    print("━" * int(H.diffs[j-1] // H.min *2-1), end="")
                print(f"{self.pointColor(V, H, V.values[i], H.values[j])}╋{self.NO_COLOR}", end="")
            print("╸" + str(v))
    
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
                    print(" " * int(H.diffs[j-1] // H.min *2-1), end="")
                print(str(h).ljust(H.just)[i], end="")
            print()

    def printGrid(self, V: Axis, H: Axis) -> None:
        """Printing out a grid

        Args:
            V (Axis): Vertical axis
            H (Axis): Horizontal axis
        """
        self.gridLegend()
        for method in (self.gridHeader, self.gridBody, self.gridFooter):
            method(V, H)
    
    def printGrids(self, top: bool = True, side: bool = True, front: bool = True) -> None:
        """Printing out a string representations of an object in a grid view

        Args:
            top (bool, optional): Render a top view? Defaults to True.
            side (bool, optional): Render a side view? Defaults to True.
            front (bool, optional): Render a front view? Defaults to True.
        """
        if not self.faces:
            return
        if top:
            self.printGrid(Axis(self, "x"), Axis(self, "y", True))
        if side:
            self.printGrid(Axis(self, "z", True), Axis(self, "y", True))
        if front:
            self.printGrid(Axis(self, "z", True), Axis(self, "x"))