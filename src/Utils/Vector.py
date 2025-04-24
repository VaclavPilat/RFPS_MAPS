## \file
# Implementations of vector classes
from . import Decorators
import math


@Decorators.addInitRepr
@Decorators.makeImmutable
@Decorators.addCopyCall("x", "y", "z")
## \todo Implement rotations for ANY degree values
# \todo Use Decimal everywhere with float trap set to True
class V3:
    """Class for representing a 3D vector, similar to a Unity3D implementation of Vector3

    This class is made to be immutable and have an automatic __repr__() implementation using decorators.
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        """Initializing a 3D vector

        Args:
            x (float, optional): X value. Defaults to 0.
            y (float, optional): Y value. Defaults to 0.
            z (float, optional): Z value. Defaults to 0.
        
        Examples:
            >>> V3(1, 2, 3)
            V3(1, 2, 3)
            >>> V3(z=3)
            V3(z=3)
        """
        ## Value of the X axis
        self.x = x
        ## Value of the Y axis
        self.y = y
        ## Value of the Z axis
        self.z = z

    def __iter__(self):
        """Iterating over values

        Returns:
            Iterator representing vector values

        Examples:
            >>> list(V3(1, 2, 3))
            [1, 2, 3]
        """
        return iter((self.x, self.y, self.z))

    def __str__(self) -> str:
        """Converting a V3 object to a string

        Returns:
            str: String representation of a vector
        
        Examples:
            >>> str(V3(1, 2, 3))
            '(1, 2, 3)'
        """
        return "(" + ", ".join([str(a) for a in list(self)]) + ")"

    def __hash__(self) -> int:
        """Getting the hash of this vector

        Returns:
            Hash representation of this vector
        
        Examples:
            >>> hash(V3(1, 2, 3))
            529344067295497451
        """
        return hash(tuple(self))

    def __eq__(self, other: "V3") -> bool:
        """Comparing this vector to another one

        Args:
            other (V3): Other vector

        Returns:
            bool: True if both have the same values
        
        Examples:
            >>> V3(1, 2, 3) == V3(1, 2, 3)
            True
            >>> V3(1, 2, 3) == V3(1, 3, 2)
            False
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
        
        Examples:
            >>> V3(1, 2, 3) + V3(-5, 8, 14)
            V3(-4, 10, 17) 
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
        
        Examples:
            >>> V3(1, 2, 3) - V3(-3, 2, 5)
            V3(4, 0, -2)
        """
        if not isinstance(other, self.__class__):
            raise ValueError("Other value is not a vector")
        return V3(*(a - b for a, b in zip(self, other)))

    def __mul__(self, other: float) -> "V3":
        """Multiplication of a vector by a number

        Args:
            other (float): Number to multiply by

        Returns:
            V3: Product of this vector and the number
        
        Examples:
            >>> V3(1, 2, 3) * 0
            V3(0, 0, 0)
            >>> V3(1, 2, 3) * 1
            V3(1, 2, 3)
            >>> V3(1, 2, 3) * 2
            V3(2, 4, 6)
        """
        if type(other) in (int, float):
            return V3(*([other * a for a in self]))
        raise ValueError("Other value is not a vector or a number")

    def __rmul__(self, other: float) -> "V3":
        """Multiplication of a vector by a number

        Args:
            other (float): Number to multiply by

        Returns:
            V3: Product of this vector and the number
        
        Examples:
            >>> 0 * V3(1, 2, 3)
            V3(0, 0, 0)
            >>> 1 * V3(1, 2, 3)
            V3(1, 2, 3)
            >>> 2 * V3(1, 2, 3)
            V3(2, 4, 6)
        """
        return self.__mul__(other)

    def __truediv__(self, other: float) -> "V3":
        """Division of a vector by a number

        Args:
            other (float): Number to divide by

        Returns:
            V3: Quotient of this vector and the number
        
        Examples:
            >>> V3(1, 2, 3) / 1
            V3(1.0, 2.0, 3.0)
            >>> V3(1, 2, 3) / 2
            V3(0.5, 1.0, 1.5)
        """
        if type(other) in (int, float):
            return V3(*([a / other for a in self]))
        raise ValueError("Other value is not a number")

    ## \note Currently only supports float as an argument
    # \todo Add multiple axis rotation: >>> V3() >> V3()
    def __rshift__(self, angle: float) -> "V3":
        """Rotating the vector on Z axis, clockwise

        Args:
            angle (float): Rotation angle in degrees

        Returns:
            V3: Rotated vector
        
        Examples:
            >>> V3(1, 2, 3) >> 0
            V3(1, 2, 3)
            >>> V3(1, 2, 3) >> 90
            V3(2, -1, 3)
            >>> V3(1, 2, 3) >> 180
            V3(-1, -2, 3)
            >>> V3(1, 2, 3) >> 270
            V3(-2, 1, 3)
        """
        assert angle % 90 == 0, "Vector only supports rotations by multiples of 90 degrees"
        angle %= 360
        if angle == 90:
            return V3(self.y, -self.x, self.z)
        if angle == 180:
            return V3(-self.x, -self.y, self.z)
        if angle == 270:
            return V3(-self.y, self.x, self.z)
        return self

    ## \note Same behaviour as __rshift__
    def __lshift__(self, angle: float) -> "V3":
        """Rotating the vector on Z axis, counter-clockwise

        Args:
            angle (float): Rotation angle in degreees

        Returns:
            V3: Rotated vector
        
        Examples:
            >>> V3(1, 2, 3) << 0
            V3(1, 2, 3)
            >>> V3(1, 2, 3) << 90
            V3(-2, 1, 3)
            >>> V3(1, 2, 3) << 180
            V3(-1, -2, 3)
            >>> V3(1, 2, 3) << 270
            V3(2, -1, 3)
        """
        return self.__rshift__(-angle)

    def __abs__(self) -> float:
        """Calculating the magnitude of the vector

        Returns:
            float: Magnitude of a vector
        
        Examples:
            >>> abs(V3())
            0.0
            >>> abs(V3(3, 4, 0))
            5.0
            >>> abs(V3(z=10))
            10.0
            >>> abs(V3(10, 10, 10))
            17.320508075688775
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    ## \todo Either change behaviour or remove
    def __contains__(self, other: "V3") -> bool:
        """Checking whether a vector "is somewhat heading the same way" as the other one

        Args:
            other (V3): Other vector whose "direction" is being checked

        Returns:
            bool: True if this vector has greater or equal values of all non-zero values of the other vector
        
        Examples:
            >>> V3() in V3(1, 2, 3)
            True
            >>> V3(0, 2, 1) in V3(1, 2, 3)
            True
            >>> V3(5) in V3(10)
            True
            >>> V3(-5) in V3(10)
            False
            >>> V3(4, 5, 6) in V3(-4, 5, 6)
            False
        """
        for a, b in zip(self, other):
            if b != 0:
                if (a > 0 and b > 0) or (a < 0 and b < 0):
                    if abs(a) < abs(b):
                        return False
                else:
                    return False
        return True


## Zero-filled vector, equals to V3(0, 0, 0)
V3.ZERO = V3()
## One-filled vector, equals to V3(1, 1, 1)
V3.ONE = V3(1, 1, 1)
## Forward direction vector, equals to V3(1, 0, 0)
V3.FORWARD = V3(x=1)
## Backward direction vector, equals to V3(-1, 0, 0)
V3.BACKWARD = V3(x=-1)
## Left direction vector, equals to V3(0, 1, 0)
V3.LEFT = V3(y=1)
## Right direction vector, equals to V3(0, -1, 0)
V3.RIGHT = V3(y=-1)
## Up direction vector, equals to V3(0, 0, 1)
V3.UP = V3(z=1)
## Down direction vector, equals to V3(0, 0, -1)
V3.DOWN = V3(z=-1)