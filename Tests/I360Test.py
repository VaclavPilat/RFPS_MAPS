## \file
# Testing the implementation of an I360 interval
from Math.Interval import I360
import unittest



# \todo Add normal+inversion count test
class I360Test(unittest.TestCase):
    """Class for testing I360 implementation
    """

    def test_contains(self) -> None:
        """Testing in operator on intervals
        """
        self.assertTrue(20 in I360())
        self.assertTrue(20 in I360(20, 100))
        self.assertTrue(20 not in I360(20, 100, includeLower=False))
        self.assertTrue(0 not in I360(20, 100))
        self.assertTrue(360 not in I360(0, 0))
        self.assertTrue(0 in I360(0, 0))
        self.assertTrue(360 not in I360(180, 360, includeUpper=False))

    def test_include(self) -> None:
        """Testing point generation with/without including bounds
        """
        x = I360(includeLower=True, includeUpper=True)
        self.assertEqual(x.generate(1), [0, 0])
        self.assertEqual(x.generate(2), [0, 180, 0])
        self.assertEqual(x.generate(3), [0, 120, 240, 0])
        x = I360(includeLower=True, includeUpper=False)
        self.assertEqual(x.generate(1), [0])
        self.assertEqual(x.generate(2), [0, 180])
        self.assertEqual(x.generate(3), [0, 120, 240])
        x = I360(includeLower=False, includeUpper=True)
        self.assertEqual(x.generate(1), [0])
        self.assertEqual(x.generate(2), [180, 0])
        self.assertEqual(x.generate(3), [120, 240, 0])
        x = I360(includeLower=False, includeUpper=False)
        self.assertEqual(x.generate(1), [])
        self.assertEqual(x.generate(2), [180])
        self.assertEqual(x.generate(3), [120, 240])
    
    def test_inversion(self) -> None:
        """Testing generation after interval inversion
        """
        self.assertEqual((~I360()).generate(100), I360(0, 0).generate(100))
        self.assertEqual((~I360(0, 180)).generate(100), I360(180, 360).generate(100))
        self.assertEqual((~I360(90, 120)).generate(100), (I360(120, 360) | I360(0, 90)).generate(100))
    
    def test_clamp(self) -> None:
        """Testing interval clamping by generating items
        """
        self.assertEqual(I360.clamp(90, 180).generate(100), I360(90, 180).generate(100))
        self.assertEqual(I360.clamp(0, 360).generate(100), I360(0, 360).generate(100))
        self.assertEqual(I360.clamp(-30, 30).generate(100), (I360(330, 360) | I360(0, 30)).generate(100))
        self.assertEqual(I360.clamp(180, 450).generate(100), (I360(180, 360) | I360(0, 90)).generate(100))
    
    def test_union(self) -> None:
        """Testing unions of intervals
        """
        self.assertEqual((I360(0, 180) | I360(60, 120)).generate(100), I360(0, 180).generate(100))
        self.assertEqual((I360(90, 270) | I360(180, 360)).generate(100), I360(90, 360).generate(100))
        self.assertEqual((I360(0, 60) | I360(90, 120)).generate(100), (I360(0, 60) | I360(90, 120)).generate(100))
    
    def test_intersect(self) -> None:
        """Testing intersections of intervals
        """
        self.assertEqual((I360(0, 180) & I360(60, 120)).generate(100), I360(60, 120).generate(100))
        self.assertEqual((I360(90, 270) & I360(180, 360)).generate(100), I360(180, 270).generate(100))
        self.assertEqual((I360(0, 60) & I360(90, 120)).generate(100), I360(0, 0, includeLower=False, includeUpper=False).generate(100))