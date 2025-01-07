## \file
# Testing Circle implementation
from Math.Shape import Circle
from Math.Data import V3, Interval
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
        circle = Circle(radius=1)
        self.assertTuplesAlmostEqual(circle(points=1).vertices(), (V3.RIGHT, ))
        self.assertTuplesAlmostEqual(circle(points=2).vertices(), (V3.RIGHT, V3.LEFT))
        self.assertTuplesAlmostEqual(circle(points=4).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD))
        with self.assertRaises(AssertionError):
            self.assertTuplesAlmostEqual(circle(points=1).vertices(), (V3.LEFT, ))
        with self.assertRaises(AssertionError):
            self.assertTuplesAlmostEqual(circle(points=2).vertices(), (V3.RIGHT, V3.RIGHT))
        with self.assertRaises(AssertionError):
            self.assertTuplesAlmostEqual(circle(points=4).vertices(), (V3.RIGHT, V3.BACKWARD, V3.LEFT, V3.FORWARD))
    
    def test_not_almost_equal(self) -> None:
        """Testing cases when generated vertices are not almost equal
        """
        circle = Circle(radius=1)
        with self.assertRaises(AssertionError):
            self.assertTuplesNotAlmostEqual(circle(points=1).vertices(), (V3.RIGHT, ))
        with self.assertRaises(AssertionError):
            self.assertTuplesNotAlmostEqual(circle(points=2).vertices(), (V3.RIGHT, V3.LEFT))
        with self.assertRaises(AssertionError):
            self.assertTuplesNotAlmostEqual(circle(points=4).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD))
        self.assertTuplesNotAlmostEqual(circle(points=1).vertices(), (V3.LEFT, ))
        self.assertTuplesNotAlmostEqual(circle(points=2).vertices(), (V3.RIGHT, V3.RIGHT))
        self.assertTuplesNotAlmostEqual(circle(points=4).vertices(), (V3.RIGHT, V3.BACKWARD, V3.LEFT, V3.FORWARD))
    
    def test_bounds(self) -> None:
        """Testing vertices generated within bounds
        """
        circle = Circle(radius=1, points=4)
        self.assertTuplesAlmostEqual(circle(bounds=Interval(0, 360)).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD, V3.RIGHT, ))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(0, 300)).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD, ))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(0, 270)).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD, ))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(0, 200)).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, ))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(0, 180)).vertices(), (V3.RIGHT, V3.FORWARD, V3.LEFT, ))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(0, 150)).vertices(), (V3.RIGHT, V3.FORWARD, ))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(0, 90)).vertices(), (V3.RIGHT, V3.FORWARD, ))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(0, 60)).vertices(), (V3.RIGHT, ))
    
    def test_advanced_bounds(self) -> None:
        """Testing advance bound usage
        """
        circle = Circle(points=4)
        self.assertTuplesAlmostEqual(circle(bounds=Interval(90, 360)).vertices(), (V3.FORWARD, V3.LEFT, V3.BACKWARD, V3.RIGHT))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(180, 270)).vertices(), (V3.LEFT, V3.BACKWARD))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(-90, 90)).vertices(), (V3.BACKWARD, V3.RIGHT, V3.FORWARD))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(-180, -90)).vertices(), (V3.LEFT, V3.BACKWARD))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(360, 450)).vertices(), (V3.RIGHT, V3.FORWARD))
        self.assertTuplesAlmostEqual(circle(bounds=Interval(450, 720)).vertices(), (V3.FORWARD, V3.LEFT, V3.BACKWARD, V3.RIGHT))