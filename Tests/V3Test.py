## \file
# Testing V3 implementation
from Math.Vector import V3
import unittest



class V3Test(unittest.TestCase):
    """Class for testing V3 implementation
    """

    def test_constructor(self) -> None:
        """Testing __init__ and __iter__ functionality
        """
        self.assertEqual(tuple(V3(1, 2, 3)), (1, 2, 3))
        self.assertEqual(V3(1, 2, 3).x, 1)
        self.assertEqual(V3(1, 2, 3).y, 2)
        self.assertEqual(V3(1, 2, 3).z, 3)
    
    def test_tostring(self) -> None:
        """Testing __str__ implementation
        """
        self.assertEqual(str(V3(1, 2, 3)), "(1, 2, 3)")
    
    def test_addition(self) -> None:
        """Testing __add__ implementation
        """
        self.assertEqual(V3(1, 2, 3) + V3(4, 5, 6), V3(5, 7, 9))
    
    def test_subtraction(self) -> None:
        """Testing __sub__ implementation
        """
        self.assertEqual(V3(1, 2, 3) - V3(4, 5, 6), V3(-3, -3, -3))
    
    def test_multiplication(self) -> None:
        """Testing __mul__ and __rmul__ implementation
        """
        self.assertEqual(V3(1, 2, 3) * 3, V3(3, 6, 9))
        self.assertEqual(3 * V3(1, 2, 3), V3(3, 6, 9))
    
    def test_division(self) -> None:
        """Testing __truediv__ implementation
        """
        self.assertEqual(V3(1, 2, 3) / 2, V3(0.5, 1, 1.5))
    
    def test_rotation(self) -> None:
        """Testing __rshift__ and __lshift__ implementation
        """
        self.assertEqual(V3.FORWARD >> 1, V3.RIGHT)
        self.assertEqual(V3.RIGHT << 2, V3.LEFT)
        self.assertEqual(V3.LEFT >> 7, V3.BACKWARD)
        self.assertEqual(V3(2, 1, 3) >> 1, V3(1, -2, 3))
        self.assertEqual(V3(1, -2, 3) >> 1, V3(-2, -1, 3))
        self.assertEqual(V3(-2, -1, 3) >> 1, V3(-1, 2, 3))
        self.assertEqual(V3(-1, 2, 3) >> 1, V3(2, 1, 3))
    
    def test_equality(self) -> None:
        """Testing __eq__ implementation
        """
        self.assertEqual(V3(1, 2, 3), V3(1, 2, 3))
        self.assertNotEqual(V3(1, 2, 3), V3(1, 2, 4))
    
    def test_copy(self) -> None:
        """Testing __call__ operator for making vector copies
        """
        self.assertEqual(V3(2, 1, 3)(), V3(2, 1, 3))
        self.assertEqual(V3(2, 1, 3)(1, 2), V3(1, 2, 3))
        a = V3(1, 2, 3)
        b = a()
        self.assertEqual(a, b)