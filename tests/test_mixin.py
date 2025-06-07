from unittest import TestCase
from dataclasses import dataclass

from parseable_dataclasses import mixin

@dataclass
class DC1(mixin.ParsearbleDataClassMixin):
    a: int

@dataclass
class DC2(mixin.ParsearbleDataClassMixin):
    a: int
    b: float
    c: str

@dataclass
class DC3(mixin.ParsearbleDataClassMixin):
    a: int
    b: float
    c: str
    d: bool = False

@dataclass
class DC4(mixin.ParsearbleDataClassMixin):
    a: list[int]

class Test_ParsearbleDataClassMixin(TestCase):
    def test_parse_dc1(self):
        expected = DC1(10)
        actual = DC1.parse_args("10".split())

        self.assertEqual(expected, actual)

    def test_parse_dc2(self):
        expected = DC2(10, 3.1415, "Hello")
        actual = DC2.parse_args("10 3.1415 Hello".split())

        self.assertEqual(expected, actual)

    def test_parse_dc3(self):
        expected = DC3(10, 3.1415, "Hello", d=True)
        actual = DC3.parse_args("--d 10 3.1415 Hello".split())

        self.assertEqual(expected, actual)
        
        expected = DC3(10, 3.1415, "Hello", d=False)
        actual = DC3.parse_args("--no-d 10 3.1415 Hello".split())

        self.assertEqual(expected, actual)

    def test_parse_dc4(self):
        expected = DC4([1, 2, 3, 4, 5, 6])
        actual = DC4.parse_args("1 2 3 4 5 6".split())

        self.assertEqual(expected, actual)
        
        expected = DC4([])
        actual = DC4.parse_args("".split())

        self.assertEqual(expected, actual)
        
        expected = DC4([0])
        actual = DC4.parse_args("0".split())

        self.assertEqual(expected, actual)
