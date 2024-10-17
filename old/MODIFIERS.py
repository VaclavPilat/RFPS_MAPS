## \file
# V3 modifiers for altering Tile vertices



from VECTOR import *



class RotateRight:
    """Modifier for rotating a vector clockwise
    """

    def __init__(self, times: int) -> None:
        """Initializing a modifier

        Args:
            times (int): How many times to rotate?
        """
        self.times = times
    
    def execute(self, vector: V3) -> V3:
        """Executing a modifier on a vector

        Args:
            vector (V3): Vector to rotate

        Returns:
            V3: Rotated vector
        """
        return vector >> self.times



class RotateLeft:
    """Modifier for rotating a vector counter-clockwise
    """

    def __init__(self, times: int) -> None:
        """Initializing a modifier

        Args:
            times (int): How many times to rotate?
        """
        self.times = times
    
    def execute(self, vector: V3) -> V3:
        """Executing a modifier on a vector

        Args:
            vector (V3): Vector to rotate

        Returns:
            V3: Rotated vector
        """
        return vector << self.times



class FlipX:
    """Modifier for flipping a vector's X axis
    """
    
    def execute(self, vector: V3) -> V3:
        """Executing a modifier on a vector

        Args:
            vector (V3): Vector to flip

        Returns:
            V3: Flipped vector
        """
        return ~vector