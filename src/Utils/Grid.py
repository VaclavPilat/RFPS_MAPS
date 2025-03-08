## \file
# Functionality for rendering Object structure in console



class Grid:
    """Functionality for rendering Object vertices in console from multiple perspectives

    Requires a subclass to have a "faces" property (a list of lists of V3 vertices)
    """

    ## Grid colors
    # ANSI colors, from coldest to hottest
    GRID_COLORS = ("\033[37m", "\033[36m", "\033[34m", "\033[32m", "\033[33m", "\033[31m", "\033[35m")

    def gridLegend(self) -> None:
        """Printing out a legend for grid colors
        """
        print(" ".join(self.GRID_COLORS[i] + str(i) for i in range(len(self.GRID_COLORS))), end="+\033[0m\n")
    
    def gridAxis(self, axis: str, reversed: bool = False) -> tuple:
        values = sorted(set(round(getattr(vertex, axis), 3) for face in self.faces for vertex in face))
        differences = [values[i] - values[i-1] for i in range(1, len(values))]
        minimum = min(differences)
        just = max(map(lambda value: len(str(value)), values))
        if reversed:
            values.reverse()
            differences.reverse()
        return (values, differences, minimum, just)
    
    def printGrid(self, Xvals, Xdiff, Xmin, Xjust, Yvals, Ydiff, Ymin, Yjust) -> None:
        # Header
        for i in range(Yjust):
            print(" " * (Xjust + 1), end="")
            for j, y in enumerate(Yvals):
                if j > 0:
                    print(" " * int(Ydiff[j-1] // Ymin *2-1), end="")
                print(str(y).rjust(Yjust)[i], end="")
            print()
        # Body
        for i, x in enumerate(Xvals):
            if i > 0:
                for j in range(int(Xdiff[i-1] // Xmin) - 1):
                    print(" " * (Xjust + 1), end="")
                    for k, y in enumerate(Yvals):
                        if k > 0:
                            print(" " * int(Ydiff[k-1] // Ymin *2-1), end="")
                        print("┃", end="")
                    print()
            print(str(x).rjust(Xjust) + "╺", end="")
            for j, y in enumerate(Yvals):
                if j > 0:
                    print("━" * int(Ydiff[j-1] // Ymin *2-1), end="")
                print("╋", end="")
            print("╸" + str(x))
        # Footer
        for i in range(Yjust):
            print(" " * (Xjust + 1), end="")
            for j, y in enumerate(Yvals):
                if j > 0:
                    print(" " * int(Ydiff[j-1] // Ymin *2-1), end="")
                print(str(y).ljust(Yjust)[i], end="")
            print()
    
    def printGrids(self, top: bool = True, side: bool = True, front: bool = True) -> None:
        """Printing out a string representations of an object in a grid view

        Args:
            top (bool, optional): Render a top view? Defaults to True.
            side (bool, optional): Render a side view? Defaults to True.
            front (bool, optional): Render a front view? Defaults to True.
        """
        if not self.faces:
            return
        self.gridLegend()
        if top:
            self.printGrid(*self.gridAxis("x"), *self.gridAxis("y", True))
        if side:
            self.printGrid(*self.gridAxis("z", True), *self.gridAxis("y", True))
        if front:
            self.printGrid(*self.gridAxis("z", True), *self.gridAxis("x"))