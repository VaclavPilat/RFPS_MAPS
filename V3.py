class V3:
    """Class for representing a 3D vector, similar to a Unity3D implementation of Vector3
    """

    def __init__(self, x: int|float = 0, y: int|float = 0, z: int|float = 0) -> None:
        """Initializing a 3D vector

        Args:
            x (int | float, optional): X. Defaults to 0.
            y (int | float, optional): Y. Defaults to 0.
            z (int | float, optional): Z. Defaults to 0.
        """
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        """Iterating over values

        Returns:
            Iterator representing vector values
        """
        return iter((self.x, self.y, self.z))

    def __str__(self) -> str:
        """Converting a V3 object to a string

        Returns:
            str: String representation of a vector
        """
        return "(" + ", ".join([str(a) for a in list(self)]) + ")"
    
    def __hash__(self):
        """Getting the hash of this vector

        Returns:
            Hash representation of this vector
        """
        return hash(tuple(self))

    def __eq__(self, other: "V3") -> bool:
        """Comparing this vector to another one

        Args:
            other (V3): Other vector

        Returns:
            bool: True if both have the same values
        """
        if not isinstance(other, self.__class__):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True
    
    def __add__(self, other: "V3") -> "V3":
        """Adding two vectors together

        Args:
            other (V3): Other vector

        Returns:
            V3: Sum of this and the other vector
        """
        if not isinstance(other, self.__class__):
            raise ValueError("Other value is not a vector")
        return V3(*(a + b for a, b in zip(self, other)))
    
    def __sub__(self, other: "V3") -> "V3":
        """Subtracting one vector from another

        Args:
            other (V3): Other vector

        Returns:
            V3: Difference of this and the other vector
        """
        if not isinstance(other, self.__class__):
            raise ValueError("Other value is not a vector")
        return V3(*(a - b for a, b in zip(self, other)))
    
    def __mul__(self, other: "V3") -> "V3":
        """Multiplication of a vector by a number or another vector

        Args:
            other (V3): Other vector or a number

        Returns:
            V3: Product of this vector and the other argument
        """
        if isinstance(other, self.__class__):
            return V3(*(a * b for a, b in zip(self, other)))
        if type(other) in (int, float):
            return V3(*([other * a for a in self]))
        raise ValueError("Other value is not a vector or a number")

V3.ZERO = V3()
V3.ONE = V3(1, 1, 1)
V3.FORWARD = V3(x=1)
V3.BACKWARD = V3(x=-1)
V3.LEFT = V3(y=1)
V3.RIGHT = V3(y=-1)
V3.UP = V3(z=1)
V3.DOWN = V3(z=-1)

if __name__ == "__main__":
    import unittest
    class V3Test(unittest.TestCase):
        def test_constructor(self):
            self.assertEqual(tuple(V3(1, 2, 3)), (1, 2, 3))
            self.assertEqual(V3(1, 2, 3).x, 1)
            self.assertEqual(V3(1, 2, 3).y, 2)
            self.assertEqual(V3(1, 2, 3).z, 3)
        def test_tostring(self):
            self.assertEqual(str(V3(1, 2, 3)), "(1, 2, 3)")
        def test_addition(self):
            self.assertEqual(V3(1, 2, 3) + V3(4, 5, 6), V3(5, 7, 9))
        def test_subtraction(self):
            self.assertEqual(V3(1, 2, 3) - V3(4, 5, 6), V3(-3, -3, -3))
        def test_multiplication(self):
            self.assertEqual(V3(1, 2, 3) * V3(4, 5, 6), V3(4, 10, 18))
            self.assertEqual(V3(1, 2, 3) * 3, V3(3, 6, 9))
        def test_presets(self):
            self.assertEqual(V3(1, 2, 3) * V3.LEFT, V3(0, 2, 0))
    unittest.main()