## \file
# Testing the implementation of an I360 interval
from Math.Interval import I360, IOperand
import unittest



class I360Test(unittest.TestCase):
    """Class for testing I360 implementation
    """

    def test_contains(self) -> None:
        """Testing in operator on intervals
        """
        self.assertTrue(20 in I360())
        self.assertTrue(20 in I360(20, 100))
        self.assertTrue(20 not in I360(20, 100, True))
        self.assertTrue(0 not in I360(20, 100))
        self.assertTrue(360 not in I360(0, 0))
        self.assertTrue(0 in I360(0, 0))
        self.assertTrue(360 not in I360(180, 360, False, True))

    def test_include(self) -> None:
        """Testing point generation with/without including bounds
        """
        x = I360()
        self.assertEqual(x[1], [0, 0])
        self.assertEqual(x[2], [0, 180, 0])
        self.assertEqual(x[3], [0, 120, 240, 0])
        x = I360(0, 360, False, True)
        self.assertEqual(x[1], [0])
        self.assertEqual(x[2], [0, 180])
        self.assertEqual(x[3], [0, 120, 240])
        x = I360(0, 360, True)
        self.assertEqual(x[1], [0])
        self.assertEqual(x[2], [180, 0])
        self.assertEqual(x[3], [120, 240, 0])
        x = I360(0, 360, True, True)
        self.assertEqual(x[1], [])
        self.assertEqual(x[2], [180])
        self.assertEqual(x[3], [120, 240])
    
    def assertIntervalGeneration(self, first: IOperand, second: IOperand, count: int = 30) -> None:
        """Asserting that both intervals generate the same points

        Args:
            first (IOperand): First interval
            second (IOperand): Second interval
            count (int, optional): Point count. Defaults to 30.
        """
        self.assertEqual(first[count], second[count])
    
    def test_inversion(self) -> None:
        """Testing generation after interval inversion
        """
        self.assertIntervalGeneration(~I360(), I360(0, 0, True, True))
        self.assertIntervalGeneration(~I360(0, 180, True), I360(180, 360, True))
        self.assertIntervalGeneration(~I360(90, 120, True, True), (I360(120, 360) | I360(0, 90)))
        self.assertIntervalGeneration(~I360(90, 120), I360(120, 360, True) | I360(0, 90, False, True))
    
    def test_clamp(self) -> None:
        """Testing interval value clamping by generating items
        """
        self.assertIntervalGeneration(I360(90, 180), I360(90, 180))
        self.assertIntervalGeneration(I360(0, 360), I360(0, 360))
        self.assertIntervalGeneration(I360(-30, 30), I360(330, 360) | I360(0, 30))
        self.assertIntervalGeneration(I360(180, 450), I360(180, 360) | I360(0, 90))
    
    def test_union(self) -> None:
        """Testing unions of intervals
        """
        self.assertIntervalGeneration(I360(0, 180) | I360(60, 120), I360(0, 180))
        self.assertIntervalGeneration(I360(90, 270) | I360(180, 360), I360(90, 360))
        self.assertIntervalGeneration(I360(0, 60) | I360(90, 120), I360(0, 60) | I360(90, 120))
    
    def test_intersect(self) -> None:
        """Testing intersections of intervals
        """
        self.assertIntervalGeneration(I360(0, 180) & I360(60, 120), I360(60, 120))
        self.assertIntervalGeneration(I360(90, 270) & I360(180, 360), I360(180, 270))
        self.assertIntervalGeneration(I360(0, 60) & I360(90, 120), I360(0, 0, True, True))
    
    def test_double_inversion(self) -> None:
        """Testing double inversion
        """
        self.assertIntervalGeneration(~~I360(0, 360), I360(0, 360))
        self.assertIntervalGeneration(~~I360(0, 180, True), I360(0, 180, True))
        self.assertIntervalGeneration(~~I360(90, 120, False, True), I360(90, 120, False, True))
        self.assertIntervalGeneration(~~I360(270, 360, True, True), I360(270, 360, True, True))
    
    def test_addition(self) -> None:
        """Testing the addition of a number to an interval
        """
        self.assertIntervalGeneration(I360(0, 180) + 90, I360(90, 270))
        self.assertIntervalGeneration(I360(60, 120, True) + 0, I360(60, 120, True))
        self.assertIntervalGeneration(I360(0, 360, True, True) + 90, I360(90, 360, True) | I360(0, 90, False, True))
        self.assertIntervalGeneration(I360(90, 120, False, True) + 360, I360(90, 120, False, True))