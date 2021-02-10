import unittest

from utilities import *


class MyTestCase(unittest.TestCase):
    def test_combine(self):
        first = "dit is een"
        second = "een korte boodschap"
        self.assertEqual("dit is een korte boodschap", combine(first, second))

        first = "dit is een"
        second = "korte boodschap"
        self.assertEqual("dit is een korte boodschap", combine(first, second))

        first = "abcde"
        second = "fghijk"
        self.assertEqual("abcdefghijk", combine(first, second, ""))

        first = ""
        second = "abc"
        self.assertEqual("abc", combine(first, second, ""))

        first = "abc"
        second = ""
        self.assertEqual("abc", combine(first, second, ""))

        first = ""
        second = ""
        self.assertEqual("check", combine(first, second, "check"))



if __name__ == '__main__':
    unittest.main()
