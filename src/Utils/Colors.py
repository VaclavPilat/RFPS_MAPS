## \file
# Variables with ANSI color strings
import sys, os


if sys.stdout.isatty() or os.getenv('COLOR'):
    ## Reset color string
    NONE = "\033[0m"
    ## Grid colors, sorted from coldest to hottest
    TEMPERATURE = ("\033[90;1m", "\033[94;1m", "\033[96;1m", "\033[92;1m", "\033[93;1m", "\033[91;1m", "\033[95;1m")
    ## Axis colors
    AXIS = {"x": "\033[91;1m", "y": "\033[92;1m", "z": "\033[94;1m"}
    ## Hierarchy colors
    HIERARCHY = ("\033[94m", "\033[95m", "\033[96m", "\033[91m", "\033[92m", "\033[93m")
    ## Bold color
    BOLD = "\033[1m"
else:
    NONE = BOLD = ""
    TEMPERATURE = HIERARCHY = ("",)
    AXIS = {"x": "", "y": "", "z": ""}


def lenANSI(string: str) -> int:
    """Getting the length of a string while ignoring ANSI escape sequences

    Args:
        string (str): String to get the length of

    Returns:
        int: Length of the pure string
    """
    for color in TEMPERATURE + tuple(AXIS.values()) + (NONE, BOLD):
        string = string.replace(color, "")
    return len(string)