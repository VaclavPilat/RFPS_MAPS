## \file
# Tests of Face functionality
from src.Utils.Mesh import Face
from src.Utils.Vector import V3
import unittest


class FaceTest(unittest.TestCase):
    """Testing Face functionality
    """

    def test_equality(self) -> None:
        """Testing face equality
        """
        self.assertEqual(Face(V3.ZERO, V3.FORWARD, V3.ONE), Face(V3.ZERO, V3.FORWARD, V3.ONE))
        self.assertEqual(Face(V3.ZERO, V3.FORWARD, V3.ONE), Face(V3.FORWARD, V3.ONE, V3.ZERO))
        self.assertNotEqual(Face(V3.ZERO, V3.FORWARD, V3.ONE), Face(V3.ZERO, V3.FORWARD, V3.ONE, V3.LEFT))
        self.assertNotEqual(Face(V3.ZERO, V3.FORWARD, V3.UP), Face(V3.ZERO, V3.FORWARD, V3.ONE))