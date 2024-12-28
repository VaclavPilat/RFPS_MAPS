## \file
# Testing Circle implementation
from Math.Circle import Circle
from Math.Vector import V3
import unittest



class CircleTest(unittest.TestCase):
    """Class for testing Circle implementation
    """

    def test_points(self) -> None:
        """Testing point counts
        """
        for i in range(1, 20 + 1):
            self.assertEqual(len(Circle(radius=1, points=i).vertices()), i)
    
    def assertTuplesAlmostEqual(self, first: tuple, second: tuple) -> None:
        """Asserting that both tuples have roughly the save vertices

        Args:
            first (tuple): First tuple
            second (tuple): Second tuple
        """
        self.assertEqual(len(first), len(second))
        for a, b in zip(first, second):
            for c, d in zip(a, b):
                self.assertAlmostEqual(c, d)
    
    def test_vertices(self) -> None:
        """Testing generated vertices
        """
        self.assertTuplesAlmostEqual(Circle(radius=1, points=1).vertices(), (V3.RIGHT, ))
        self.assertTuplesAlmostEqual(Circle(radius=1, points=2).vertices(), (V3.RIGHT, V3.LEFT))
        self.assertTuplesAlmostEqual(Circle(radius=1, points=4).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD))