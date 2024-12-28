## \file
# Testing Circle implementation
from Math.Circle import Circle
from Math.Vector import V3
import unittest



class CircleTest(unittest.TestCase):
    """Class for testing Circle implementation
    """

    def test_points(self) -> None:
        """Testing that circle returns the correct base amount of vertices
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
        for fv, sv in zip(first, second):
            for f, s in zip(fv, sv):
                self.assertAlmostEqual(f, s)
    
    def assertTuplesNotAlmostEqual(self, first: tuple, second: tuple) -> None:
        """Asserting that both tuples do not have almost equal vertices

        Args:
            first (tuple): First tuple
            second (tuple): Second tuple
        """
        self.assertEqual(len(first), len(second))
        try:
            self.assertTuplesAlmostEqual(first, second)
        except AssertionError:
            return
        self.assertTrue(False)
    
    def test_almost_equal(self) -> None:
        """Testing cases when generated vertices are almost equal
        """
        self.assertTuplesAlmostEqual(Circle(radius=1, points=1).vertices(), (V3.RIGHT, ))
        self.assertTuplesAlmostEqual(Circle(radius=1, points=2).vertices(), (V3.RIGHT, V3.LEFT))
        self.assertTuplesAlmostEqual(Circle(radius=1, points=4).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD))
        with self.assertRaises(AssertionError):
            self.assertTuplesAlmostEqual(Circle(radius=1, points=1).vertices(), (V3.LEFT, ))
        with self.assertRaises(AssertionError):
            self.assertTuplesAlmostEqual(Circle(radius=1, points=2).vertices(), (V3.RIGHT, V3.RIGHT))
        with self.assertRaises(AssertionError):
            self.assertTuplesAlmostEqual(Circle(radius=1, points=4).vertices(), (V3.RIGHT, V3.BACKWARD, V3.LEFT, V3.FORWARD))
    
    def test_not_almost_equal(self) -> None:
        """Testing cases when generated vertices are not almost equal
        """
        with self.assertRaises(AssertionError):
            self.assertTuplesNotAlmostEqual(Circle(radius=1, points=1).vertices(), (V3.RIGHT, ))
        with self.assertRaises(AssertionError):
            self.assertTuplesNotAlmostEqual(Circle(radius=1, points=2).vertices(), (V3.RIGHT, V3.LEFT))
        with self.assertRaises(AssertionError):
            self.assertTuplesNotAlmostEqual(Circle(radius=1, points=4).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD))
        self.assertTuplesNotAlmostEqual(Circle(radius=1, points=1).vertices(), (V3.LEFT, ))
        self.assertTuplesNotAlmostEqual(Circle(radius=1, points=2).vertices(), (V3.RIGHT, V3.RIGHT))
        self.assertTuplesNotAlmostEqual(Circle(radius=1, points=4).vertices(), (V3.RIGHT, V3.BACKWARD, V3.LEFT, V3.FORWARD))