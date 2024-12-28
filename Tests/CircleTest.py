## \file
# Testing Circle implementation
from Math.Circle import Circle
import unittest



class CircleTest(unittest.TestCase):
    """Class for testing Circle implementation
    """
    
    def test_points(self) -> None:
        """Testing point counts
        """
        for i in range(1, 20 + 1):
            self.assertEqual(len(Circle(radius=1, points=i).vertices()), i)