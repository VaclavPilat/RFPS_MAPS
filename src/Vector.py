## \file
# Implementations of a vector class.
# \todo Use Decimal everywhere with float trap set to True
# \todo Add multiple axis rotation: `V3 >> V3`
from . import Decorators
import math, decimal


# Preventing floats from being passed to the Decimal constructor
#decimal.getcontext().traps[decimal.FloatOperation] = True


@Decorators.addOperators
@Decorators.addInitRepr
@Decorators.makeImmutable
@Decorators.addCopyCall("x", "y", "z")
class V3:
    """Class for representing a 3D vector.

    It is similar to a Unity3D implementation of Vector3.
    The X axis is for forward/backward values, Y is for left/right and Z is for vertical values.

    Examples:
        >>> V3(1, 2, 3)
        V3(1, 2, 3)
        >>> V3(z=3)
        V3(z=3)
    """

    def __init__(self, x: decimal.Decimal = decimal.Decimal(0), y: decimal.Decimal = decimal.Decimal(0),
                 z: decimal.Decimal = decimal.Decimal(0)) -> None:
        """Initializing a 3D vector

        Args:
            x (decimal.Decimal, optional): X value. Defaults to decimal.Decimal(0).
            y (decimal.Decimal, optional): Y value. Defaults to decimal.Decimal(0).
            z (decimal.Decimal, optional): Z value. Defaults to decimal.Decimal(0).
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
            >>> list(V3(1, 2, 3)) == list(V3(1, 2, 3))
            True
            >>> list(V3(1, 2, 3)) == list(V3(1, 2, 2))
            False
        """
        yield self.x
        yield self.y
        yield self.z

    def __str__(self) -> str:
        """Converting a V3 object to a string

        Returns:
            str: String representation of a vector
        
        Examples:
            >>> str(V3(1, 2, 3))
            '(1, 2, 3)'
        """
        return f"({', '.join(map(str, self))})"

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
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neg__(self) -> "V3":
        """Negating this vector

        Returns:
            V3: Vector with negated axis values

        Examples:
            >>> -V3(3, -5, 8) == V3(-3, 5, -8)
            True
        """
        return V3(-self.x, -self.y, -self.z)

    def __add__(self, other: "V3") -> "V3":
        """Adding two vectors together

        Args:
            other (V3): Other vector

        Returns:
            V3: Sum of this and the other vector
        
        Examples:
            >>> V3(1, 2, 3) + V3(-5, 8, 14) == V3(-4, 10, 17)
            True
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return V3(*(a + b for a, b in zip(self, other)))

    def __mul__(self, other: decimal.Decimal) -> "V3":
        """Multiplication of a vector by a number

        Args:
            other (decimal.Decimal): Number to multiply by

        Returns:
            V3: Product of this vector and the number
        
        Examples:
            >>> V3(1, 2, 3) * 0 == V3(0, 0, 0)
            True
            >>> V3(1, 2, 3) * 1 == V3(1, 2, 3)
            True
            >>> V3(1, 2, 3) * 2 == V3(2, 4, 6)
            True
        """
        return V3(*(other * a for a in self))

    def __truediv__(self, other: decimal.Decimal) -> "V3":
        """Division of a vector by a number

        Args:
            other (float): Number to divide by

        Returns:
            V3: Quotient of this vector and the number
        
        Examples:
            >>> V3(1, 2, 3) / 1 == V3(1.0, 2.0, 3.0)
            True
            >>> V3(1, 2, 3) / 2 == V3(0.5, 1.0, 1.5)
            True
        """
        return V3(*(a / other for a in self))

    def __rshift__(self, other: decimal.Decimal) -> "V3":
        """Rotating the vector on Z axis, clockwise

        Args:
            other (decimal.Decimal): Rotation angle in degrees

        Returns:
            V3: Rotated vector
        
        Examples:
            >>> V3(1, 2, 3) >> 0 == V3(1, 2, 3)
            True
            >>> V3(1, 2, 3) >> 90 == V3(2, -1, 3)
            True
            >>> V3(1, 2, 3) >> 180 == V3(-1, -2, 3)
            True
            >>> V3(1, 2, 3) >> 270 == V3(-2, 1, 3)
            True
        """
        if other % 90 != 0:
            return NotImplemented
        other %= 360
        if other == 90:
            return V3(self.y, -self.x, self.z)
        if other == 180:
            return V3(-self.x, -self.y, self.z)
        if other == 270:
            return V3(-self.y, self.x, self.z)
        return self

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

    def __matmul__(self, other: "V3") -> "V3":
        """Calculating the cross product of two vectors

        Args:
            other (V3): Other vector

        Returns:
            V3: Cross product of two vectors

        Examples:
            >>> V3(1, 2, 3) @ V3(1, 2, 3) == V3(0, 0, 0)
            True
            >>> V3(1, 2, 3) @ V3(4, 5, 6) == V3(-3, 6, -3)
            True
            >>> V3(1, 2, 3) @ V3(-1, -2, -3) == V3(0, 0, 0)
            True
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        return V3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __bool__(self) -> bool:
        """Checking whether the vector is non-zero

        Returns:
            bool: True if the vector is not equal to V3(0, 0, 0)

        Examples:
            >>> bool(V3(1, 2, 3))
            True
            >>> bool(V3(0, 1, 0))
            True
            >>> bool(V3(0, 0, 0))
            False
        """
        return self.x != 0 or self.y != 0 or self.z != 0


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