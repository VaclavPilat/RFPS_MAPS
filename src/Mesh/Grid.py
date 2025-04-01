## \file
# Functionality for rendering Object structure in console
from Utils.Decorators import makeImmutable
from Utils.Colors import NONE, AXIS, TEMPERATURE, lenANSI
from Math.Vector import V3
import math, re



@makeImmutable
class Grid:
    """Class for rendering 3D objects in a 2D grid, with multiple possible perspectives
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
        while self.queue:
            obj, layer = queue.pop(0)
            if layer == len(vertices):
                vertices.append(set())
            for face in obj.faces:
                for vertex in face:
                    vertices[layer].add(vertex)
            for child in obj:
                queue.append((child, layer + 1))
        return tuple(vertices)
    
    def print(self, vertical: str, horizontal: str, depth: int = 0) -> None:
        """Printing out a grid

        Args:
            vertical (str): Vertical axis name
            horizontal (str): Horizontal axis name
            depth (int, optional): Maximum layer index. Defaults to 0.
        """
        assert depth >= 0, "Max depth cannot be a negative number"
        for axis in (vertical, horizontal):
            assert re.fullmatch("-?[xyz]", axis), "Invalid axis name"