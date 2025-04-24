## \file
# Line implementation tests
from src.Utils.Mesh import Line
from src.Utils.Vector import V3
import unittest


class LineTest(unittest.TestCase):
    """Class for testing Line implementation.
    """

    def test_constructor(self) -> None:
        """Testing Line constructor
        """
        Line(V3.ZERO, V3.ONE)
        with self.assertRaises(ValueError):
            Line(V3.ZERO, V3.ZERO)

    def test_call(self) -> None:
        """Testing Line copy call
        """
        with self.assertRaises(ValueError):
            Line(V3.ONE, V3.FORWARD)(0, 0, 0)
        self.assertEqual(Line(V3.ONE, V3.FORWARD)(), Line(V3.ONE, V3.FORWARD))
        self.assertEqual(Line(V3.ONE, V3.FORWARD)(x=0), Line(V3.LEFT + V3.UP, V3.ZERO))

    def test_equality(self) -> None:
        """Testing Line equality
        """
        self.assertEqual(Line(V3.ZERO, V3.ONE), Line(V3.ZERO, V3.ONE))
        self.assertEqual(Line(V3.ZERO, V3.ONE), Line(V3.ONE, V3.ZERO))
        self.assertNotEqual(Line(V3.ZERO, V3.ONE), Line(V3.FORWARD, V3.ONE))
        self.assertNotEqual(Line(V3.ZERO, V3.ONE), Line(V3.ZERO, V3.FORWARD))

    def test_hash(self) -> None:
        """Testing Line hashing
        """
        self.assertFalse(Line(V3.ZERO, V3.ONE) in set())
        self.assertTrue(Line(V3.ZERO, V3.ONE) in {Line(V3.ZERO, V3.ONE), })
        self.assertTrue(Line(V3.ONE, V3.ZERO) in {Line(V3.ZERO, V3.ONE), })
        self.assertFalse(Line(V3.ONE, V3.ZERO) in {Line(V3.ZERO, V3.FORWARD), })

    def test_increment(self) -> None:
        """Testing Line increment
        """
        self.assertEqual(Line(V3.ZERO, V3.ONE) + V3.UP, Line(V3.UP, V3.ONE + V3.UP))
        self.assertEqual(Line(V3.UP * 2, V3.DOWN) + V3.UP, Line(V3.ZERO, V3.UP * 3))

    def test_rotation(self) -> None:
        """Testing Line rotations
        """
        self.assertEqual(Line(V3.RIGHT * 2, V3.FORWARD * 3) >> 90, Line(V3.BACKWARD * 2, V3.RIGHT * 3))
        self.assertEqual(Line(V3.ONE * 2, V3.LEFT * 3) >> 360, Line(V3.LEFT * 3, V3.ONE * 2))