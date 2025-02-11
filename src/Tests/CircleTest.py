## \file
# Testing Circle implementation
from Math.Shape import Circle
from Math.Vector import V3
from Math.Interval import I360
import unittest



## \todo Add face tests
# \todo Add cylinder tests
class CircleTest(unittest.TestCase):
    """Class for testing Circle implementation
    """

    def test_points(self) -> None:
        """Testing that circle returns the correct base amount of vertices
        """
        for points in [2**i for i in range(1, 10)]:
            self.assertEqual(len(tuple(Circle(radius=1, bounds=I360(points=points)))), points)
    
    def assertVerticesEqual(self, first: Circle, second: tuple) -> None:
        """Asserting that both tuples have roughly the same vertices

        Args:
            first (tuple): First tuple
            second (tuple): Second tuple
        """
        self.assertEqual(len(tuple(first)), len(second))
        for fv, sv in zip(first, second):
            for f, s in zip(fv, sv):
                self.assertAlmostEqual(f, s)
    
    def assertVerticesNotEqual(self, first: Circle, second: tuple) -> None:
        """Asserting that both tuples do not have almost equal vertices

        Args:
            first (tuple): First tuple
            second (tuple): Second tuple
        """
        self.assertEqual(len(tuple(first)), len(second))
        try:
            self.assertVerticesEqual(first, second)
        except AssertionError:
            return
        self.assertTrue(False)
    
    def test_almost_equal(self) -> None:
        """Testing cases when generated vertices are almost equal
        """
        circle = Circle()
        self.assertVerticesEqual(circle(bounds=I360(points=1)), (V3.RIGHT, ))
        self.assertVerticesEqual(circle(bounds=I360(points=2)), (V3.RIGHT, V3.LEFT))
        self.assertVerticesEqual(circle(bounds=I360(points=4)), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD))
        with self.assertRaises(AssertionError):
            self.assertVerticesEqual(circle(bounds=I360(points=1)), (V3.LEFT, ))
        with self.assertRaises(AssertionError):
            self.assertVerticesEqual(circle(bounds=I360(points=2)), (V3.RIGHT, V3.RIGHT))
        with self.assertRaises(AssertionError):
            self.assertVerticesEqual(circle(bounds=I360(points=4)), (V3.RIGHT, V3.BACKWARD, V3.LEFT, V3.FORWARD))
    
    def test_not_almost_equal(self) -> None:
        """Testing cases when generated vertices are not almost equal
        """
        circle = Circle()
        with self.assertRaises(AssertionError):
            self.assertVerticesNotEqual(circle(bounds=I360(points=1)), (V3.RIGHT, ))
        with self.assertRaises(AssertionError):
            self.assertVerticesNotEqual(circle(bounds=I360(points=2)), (V3.RIGHT, V3.LEFT))
        with self.assertRaises(AssertionError):
            self.assertVerticesNotEqual(circle(bounds=I360(points=4)), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD))
        self.assertVerticesNotEqual(circle(bounds=I360(points=1)), (V3.LEFT, ))
        self.assertVerticesNotEqual(circle(bounds=I360(points=2)), (V3.RIGHT, V3.RIGHT))
        self.assertVerticesNotEqual(circle(bounds=I360(points=4)), (V3.RIGHT, V3.BACKWARD, V3.LEFT, V3.FORWARD))
    
    def test_bounds(self) -> None:
        """Testing vertices generated within bounds
        """
        circle = Circle()
        self.assertVerticesEqual(circle(bounds=I360(0, 360, points=4)), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD, ))
        self.assertVerticesEqual(circle(bounds=I360(0, 300, points=4)), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD, ))
        self.assertVerticesEqual(circle(bounds=I360(0, 270, points=4)), (V3.RIGHT, V3.FORWARD, V3.LEFT, V3.BACKWARD, ))
        self.assertVerticesEqual(circle(bounds=I360(0, 200, points=4)), (V3.RIGHT, V3.FORWARD, V3.LEFT, ))
        self.assertVerticesEqual(circle(bounds=I360(0, 180, points=4)), (V3.RIGHT, V3.FORWARD, V3.LEFT, ))
        self.assertVerticesEqual(circle(bounds=I360(0, 150, points=4)), (V3.RIGHT, V3.FORWARD, ))
        self.assertVerticesEqual(circle(bounds=I360(0, 90, points=4)), (V3.RIGHT, V3.FORWARD, ))
        self.assertVerticesEqual(circle(bounds=I360(0, 60, points=4)), (V3.RIGHT, ))
    
    def test_advanced_bounds(self) -> None:
        """Testing advanced bound usage
        """
        circle = Circle()
        self.assertVerticesEqual(circle(bounds=I360(90, 360, points=4)), (V3.FORWARD, V3.LEFT, V3.BACKWARD, V3.RIGHT))
        self.assertVerticesEqual(circle(bounds=I360(180, 270, points=4)), (V3.LEFT, V3.BACKWARD))
        self.assertVerticesEqual(circle(bounds=I360(-90, 90, points=4)), (V3.BACKWARD, V3.RIGHT, V3.FORWARD))
        self.assertVerticesEqual(circle(bounds=I360(-180, -90, points=4)), (V3.LEFT, V3.BACKWARD))
        self.assertVerticesEqual(circle(bounds=I360(360, 450, points=4)), (V3.RIGHT, V3.FORWARD))
        self.assertVerticesEqual(circle(bounds=I360(450, 720, points=4)), (V3.FORWARD, V3.LEFT, V3.BACKWARD, V3.RIGHT))