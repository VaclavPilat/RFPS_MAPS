## \file
# Functionality for rendering Object structure in console



class Grid:
    """Functionality for rendering Object vertices in console from multiple perspectives
    """
    
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
    
    def printGrids(self) -> None:
        """Printing out a string representation of an object in a grid view
        """
        if not self.faces:
            return
        self.printGrid(*self.gridAxis("x"), *self.gridAxis("y", True))
        self.printGrid(*self.gridAxis("z", True), *self.gridAxis("y", True))
        self.printGrid(*self.gridAxis("z", True), *self.gridAxis("x"))