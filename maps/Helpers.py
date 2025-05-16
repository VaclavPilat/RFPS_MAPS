## \file
# Small helpful constructs that don't fit anywhere else.
# \todo Add tests and better docstrings
from . import Decorators
import time


class Repr(type):
    """Custom type for having a __repr__ method that returns type name
    """

    def __repr__(cls) -> str:
        """Returns name of current type

        Returns:
            str: Name of the current type
        """
        return cls.__name__


@Decorators.makeImmutable
class Settings:
    """Class for containing readonly object settings
    """

    def __init__(self, **kwargs) -> None:
        """Initialising a Settings instance with kwarg values
        """
        for key, value in kwargs.items():
            setattr(self, key, value)


def elapsedTime(function):
    """Decorator for measuring time spent on a function call and printing it out

    Args:
        function (function): Function whose calls are being examined
    """

    def wrapped(*args, **kwargs):
        start = time.time()
        output = function(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{function.__name__}() - {round(elapsed, 3)}s")
        return output

    return wrapped