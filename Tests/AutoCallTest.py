## \file
# Testing the logic of the autoCall decorator
from Utils.Wrapper import autoCall
import unittest



@autoCall("number", "string", "boolean")
class Wrapped:
    """Example class being wrapped
    """

    def __init__(self, number: int, string: str, boolean: bool) -> None:
        """Initialising object fields

        Args:
            number (int): Number value
            string (str): String value
            boolean (bool): Bool value
        """
        self.number = number
        self.string = string
        self.boolean = boolean



class AutoCallTest(unittest.TestCase):
    """Class for testing autoCall behaviour
    """

    def test_value(self) -> None:
        """Testing initial object values
        """
        x = Wrapped(10, "foo", True)
        self.assertEqual(x.number, 10)
        self.assertEqual(x.string, "foo")
        self.assertEqual(x.boolean, True)
    
    def test_empty(self) -> None:
        """Testing __call__ with an empty constructor
        """
        x = Wrapped(10, "foo", True)()
        self.assertEqual(x.number, 10)
        self.assertEqual(x.string, "foo")
        self.assertEqual(x.boolean, True)
    
    def test_args(self) -> None:
        """Testing __call__ with args only
        """
        x = Wrapped(10, "foo", True)(20, "bar")
        self.assertEqual(x.number, 20)
        self.assertEqual(x.string, "bar")
        self.assertEqual(x.boolean, True)
    
    def test_kwargs(self) -> None:
        """Testing __call__ with kwargs only
        """
        x = Wrapped(10, "foo", True)(string="bar", number=40)
        self.assertEqual(x.number, 40)
        self.assertEqual(x.string, "bar")
        self.assertEqual(x.boolean, True)
    
    def test_both(self) -> None:
        """Testing __call__ with both args and kwargs at the same time
        """
        x = Wrapped(10, "foo", True)(-5, "baz", boolean=False)
        self.assertEqual(x.number, -5)
        self.assertEqual(x.string, "baz")
        self.assertEqual(x.boolean, False)