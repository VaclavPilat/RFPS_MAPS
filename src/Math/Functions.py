## \file
# Various math functions
import math



def isPow2(number: int) -> bool:
    """Checking whether a number is a power of 2

    Args:
        number (int): Integer number to check

    Returns:
        bool: True if the number of a power of 2
    """
    return (number & (number-1) == 0) and number > 0