"""! \file
Small helpful constructs that don't fit anywhere else.
"""
import time


class Repr(type):
    """Custom type for having a __repr__ method that returns type name

    Examples:
        >>> class Foo(metaclass=Repr):
        ...     pass
        ...
        >>> repr(Foo)
        'Foo'
    """

    def __repr__(cls) -> str:
        """Returns name of current type

        Returns:
            str: Name of the current type
        """
        return cls.__name__


def stopwatch(function):
    """Decorator for measuring time spent on a function call and printing it out

    Args:
        function (function): Function whose calls are being examined

    Returns:
        function: Wrapped function
    """

    def wrapped(*args, **kwargs):
        start = time.time()
        output = function(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{function.__name__}() - {round(elapsed, 3)}s")
        return output

    return wrapped