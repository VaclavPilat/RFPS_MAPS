## \file
# Collection of static math functions



class Math:
    """General math functions
    """

    @staticmethod
    def isPow2(number: int) -> bool:
        """Checking whether a number is a power of 2

        Args:
            number (int): Number to check

        Returns:
            bool: True if the number is a non-zero power of 2
        """
        return number > 0 and (number & (number - 1)) == 0
    
    @staticmethod
    def average(*args) -> float:
        """Calculating average of numbers

        Returns:
            float: Average number
        """
        return sum(args) / len(args)