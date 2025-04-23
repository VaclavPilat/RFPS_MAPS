## \file
# Classes and various other small helpful constructs
from .Decorators import *


class Repr(type):
    """Custom type for having a __repr__ method that returns type name
    """

    def __repr__(cls) -> str:
        """Returns name of current type

        Returns:
            str: Name of the current type
        """
        return cls.__name__


@makeImmutable
class Settings:
    """Class for containing readonly object settings
    """

    def __init__(self, **kwargs) -> None:
        """Initialising a Settings instance with kwarg values
        """
        for key, value in kwargs.items():
            setattr(self, key, value)