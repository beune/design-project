import unittest

from utilities import *


class MyTestCase(unittest.TestCase):
    def test_combine(self):
        # combine two overlapping strings
        first = "dit is een"
        second = "een korte boodschap"
        self.assertEqual("dit is een korte boodschap", combine(first, second))

        # append the strings if no overlap
        first = "dit is een"
        second = "korte boodschap"
        self.assertEqual("dit is een korte boodschap", combine(first, second))

        first = "abcde"
        second = "fghijk"
        self.assertEqual("abcdefghijk", combine(first, second, ""))

        # don't fail if something is empty
        first = ""
        second = "abc"
        self.assertEqual("abc", combine(first, second, ""))

        first = "abc"
        second = ""
        self.assertEqual("abc", combine(first, second, ""))

        first = ""
        second = ""
        self.assertEqual("check", combine(first, second, "check"))

        # combine the largest amount of characters
        first = "ho ho ho"
        second = "ho ho merry crisis"
        self.assertEqual("ho ho ho merry crisis", combine(first, second))



if __name__ == '__main__':
    unittest.main()
