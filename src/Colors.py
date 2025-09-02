"""! \file
Functionality for colorizing text.

Colors will not be used if python detects that stdout is not a tty (console).
This can be overturned by setting a "COLOR" environment variable to any value.
"""
import enum, sys, os, re


## Is color mode enabled?
ENABLED = sys.stdout.isatty() or os.getenv("COLOR")


class Color (enum.Enum):
    """Enum for all defined colors in the form of ANSI codes.
    """

    ## No color (stops the effect of any previous ANSI code)
    NONE = "\033[0m"

    ## Bold color
    BOLD = "\033[1m"

    ## Black color
    BLACK = "\033[90m"
    ## Red color
    RED = "\033[91m"
    ## Green color
    GREEN = "\033[92m"
    ## Yellow color
    YELLOW = "\033[93m"
    ## Blue color
    BLUE = "\033[94m"
    ## Purple color
    PURPLE = "\033[95m"
    ## Cyan color
    CYAN = "\033[96m"
    ## White color
    WHITE = "\033[97m"

    ## X axis color
    X = RED
    ## Y axis color
    Y = GREEN
    ## Z axis color
    Z = BLUE

    def __str__(self) -> str:
        """Getting the color code.

        Returns:
            str: ANSI code of the color.
        """
        return self.value

    def __call__(self, text: str) -> str:
        """Colorizing a string with the specified color.

        If stdout is not a terminal or COLOR environmental variable is not set, the unmodified text is returned.

        Args:
            text (str): The string to colorize

        Returns:
            str: String wrapped in ANSI color codes
        """
        if not ENABLED or self == Color.NONE:
            return text
        return f"{self}{text}{Color.NONE}"


class Temperature (enum.Enum):
    """Enum for temperature colors that accepts out of bound indexes.

    The name corresponds to a Color member, the value is the temperature index.
    All values have to be sequentional, starting from 0.
    """

    ## Color #0
    BLACK = 0

    if ENABLED:
        ## Color #1
        BLUE = 1
        ## Color #2
        CYAN = 2
        ## Color #3
        GREEN = 3
        ## Color #4
        YELLOW = 4
        ## Color #5
        RED = 5
        ## Color #6
        PURPLE = 6

    @classmethod
    def _missing_(cls, index: int) -> "Temperature":
        """A fallback for when the Temperature index inevitably falls out of bounds.

        The provided index gets clamped and a proper member returned.

        Args:
            index (int): Out of bounds index

        Returns:
            Temperature: Existing Temperature member
        """
        if index >= len(cls):
            return Temperature(len(cls) - 1)
        return Temperature(0)

    def __call__(self, text: str) -> str:
        """Colorizing a string with the specified temperature.

        Args:
            text (str): Text to colorize

        Returns:
            str: Text wrapped in ANSI color codes
        """
        return Color[self.name](text)


class Hierarchy (enum.Enum):
    """Enum for hierarchy colors that accepts out of bound indexes.

    The name corresponds to a Color member, the value is the temperature index.
    All values have to be sequentional, starting from 0.
    """

    ## Color #0
    BLUE = 0
    ## Color #1
    PURPLE = 1
    ## Color #2
    CYAN = 2
    ## Color #3
    RED = 3
    ## Color #4
    GREEN = 4
    ## Color #5
    YELLOW = 5

    @classmethod
    def _missing_(cls, index: int) -> "Hierarchy":
        """A fallback for when the Hierarchy index inevitably falls out of bounds.

        The provided index gets clamped and a proper member returned.

        Args:
            index (int): Out of bounds index

        Returns:
            Hierarchy: Existing Hierarchy member
        """
        return Hierarchy(index % len(Hierarchy))

    def __call__(self, text: str) -> str:
        """Colorizing a string with the specified hierarchy.

        Args:
            text (str): Text to colorize

        Returns:
            str: Text wrapped in ANSI color codes
        """
        return Color[self.name](text)


def alen(string: str) -> int:
    """Getting the length of a string while ignoring ANSI escape sequences

    Args:
        string (str): String to get the length of

    Returns:
        int: Length of the pure string
    """
    return len(re.sub("\\033\[\d+;?\d*m", "", string))