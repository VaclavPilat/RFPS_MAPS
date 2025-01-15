## \file
# Testing the implementation of an I360 interval
from Math.Interval import I360, IOperand
import unittest



## \todo Test HALF* and QUARTER* instances
## \todo More robust addition and subtraction testing
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
        self.assertEqual(x[1], [0])
        self.assertEqual(x[2], [0, 180])
        self.assertEqual(x[3], [0, 120, 240])
        x = I360(0, 360, False, True)
        self.assertEqual(x[1], [0])
        self.assertEqual(x[2], [0, 180])
        self.assertEqual(x[3], [0, 120, 240])
        x = I360(0, 360, True)
        self.assertEqual(x[1], [])
        self.assertEqual(x[2], [180])
        self.assertEqual(x[3], [120, 240])
        x = I360(0, 360, True, True)
        self.assertEqual(x[1], [])
        self.assertEqual(x[2], [180])
        self.assertEqual(x[3], [120, 240])
    
    def assertIntervalEqual(self, first: IOperand, second: IOperand, count: int = 30) -> None:
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
        self.assertIntervalEqual(~I360(), I360(0, 0, True, True))
        self.assertIntervalEqual(~I360(0, 180, True), I360(180, 360, True))
        self.assertIntervalEqual(~I360(90, 120, True, True), (I360(120, 360) | I360(0, 90)))
        self.assertIntervalEqual(~I360(90, 120), I360(120, 360, True) | I360(0, 90, False, True))
    
    def test_clamp(self) -> None:
        """Testing interval value clamping by generating items
        """
        self.assertIntervalEqual(I360(90, 180), I360(90, 180))
        self.assertIntervalEqual(I360(0, 360), I360(0, 360))
        self.assertIntervalEqual(I360(-30, 30), I360(330, 360) | I360(0, 30))
        self.assertIntervalEqual(I360(180, 450), I360(180, 360) | I360(0, 90))
    
    def test_union(self) -> None:
        """Testing unions of intervals
        """
        self.assertIntervalEqual(I360(0, 180) | I360(60, 120), I360(0, 180))
        self.assertIntervalEqual(I360(90, 270) | I360(180, 360), I360(90, 360))
        self.assertIntervalEqual(I360(0, 60) | I360(90, 120), I360(0, 60) | I360(90, 120))
    
    def test_intersect(self) -> None:
        """Testing intersections of intervals
        """
        self.assertIntervalEqual(I360(0, 180) & I360(60, 120), I360(60, 120))
        self.assertIntervalEqual(I360(90, 270) & I360(180, 360), I360(180, 270))
        self.assertIntervalEqual(I360(0, 60) & I360(90, 120), I360(0, 0, True, True))
    
    def test_double_inversion(self) -> None:
        """Testing double inversion
        """
        self.assertIntervalEqual(~~I360(0, 360), I360(0, 360))
        self.assertIntervalEqual(~~I360(0, 180, True), I360(0, 180, True))
        self.assertIntervalEqual(~~I360(90, 120, False, True), I360(90, 120, False, True))
        self.assertIntervalEqual(~~I360(270, 360, True, True), I360(270, 360, True, True))
    
    def test_addition(self) -> None:
        """Testing the addition of a number to an interval
        """
        self.assertIntervalEqual(I360(0, 180) + 90, I360(90, 270))
        self.assertIntervalEqual(I360(60, 120, True) + 0, I360(60, 120, True))
        self.assertIntervalEqual(I360(0, 360, True, True) + 90, I360(90, 360, True) | I360(0, 90, False, True))
        self.assertIntervalEqual(I360(90, 120, False, True) + 360, I360(90, 120, False, True))
    
    def test_full_empty(self) -> None:
        """Testing the behaviour of FULL and EMPTY instances
        """
        self.assertIntervalEqual(I360(openStart=False, openEnd=False), I360.FULL)
        self.assertIntervalEqual(I360(openStart=False, openEnd=True), I360.FULL)
        self.assertIntervalEqual(I360.FULL | I360.FULL, I360.FULL)
        self.assertIntervalEqual(I360.FULL & I360.FULL, I360.FULL)
        self.assertIntervalEqual(I360.EMPTY | I360.EMPTY, I360.EMPTY)
        self.assertIntervalEqual(I360.EMPTY & I360.EMPTY, I360.EMPTY)
        self.assertIntervalEqual(I360.FULL & I360.EMPTY, I360.EMPTY)
        self.assertIntervalEqual(I360.FULL | I360.EMPTY, I360.FULL)
        self.assertIntervalEqual(~I360.FULL, I360.EMPTY)
        self.assertIntervalEqual(~I360.EMPTY, I360.FULL)
        for i in range(0, 360 + 1, 90):
            self.assertIntervalEqual(I360.EMPTY + i, I360.EMPTY)
            self.assertIntervalEqual(I360.FULL + i, I360.FULL)
    
    def test_halves(self) -> None:
        """Testing the behaviour of HALF1 and 2 instances
        """
        self.assertIntervalEqual(I360.HALF1 | I360.HALF2, I360.FULL)
        self.assertIntervalEqual(I360.HALF1 & I360.HALF2, I360(0, 0) | I360(180, 180))