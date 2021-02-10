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

        first = "dit is een test die de implement"
        second = "die de implementatie laat zien van het nieuwe algoritme"
        self.assertEqual("dit is een test die de implementatie laat zien van het nieuwe algoritme", combine(first, second))

        first = "dit is een lekker systeem"
        second = "maar het werkt niet zo goed"
        self.assertEqual("dit is een lekker systeem maar het werkt niet zo goed",
                         combine(first, second))


    def test_combine_word(self):

        # combine two overlapping strings
        first = "dit is een"
        second = "een korte boodschap"
        self.assertEqual("dit is een korte boodschap", combine_word(first, second))

        # append the strings if no overlap
        first = "dit is een"
        second = "korte boodschap"
        self.assertEqual("dit is een korte boodschap", combine_word(first, second))

        first = "abcde"
        second = "fghijk"
        self.assertEqual("abcdefghijk", combine_word(first, second, ""))

        # don't fail if something is empty
        first = ""
        second = "abc"
        self.assertEqual("abc", combine_word(first, second, ""))

        first = "abc"
        second = ""
        self.assertEqual("abc", combine_word(first, second, ""))

        first = ""
        second = ""
        self.assertEqual("check", combine_word(first, second, "check"))

        # combine the largest amount of characters
        first = "ho ho ho"
        second = "ho ho merry crisis"
        self.assertEqual("ho ho ho merry crisis", combine_word(first, second))

        first = "dit is een lekker systeem"
        second = "maar het werkt niet zo goed"
        self.assertEqual("dit is een lekker systeem maar het werkt niet zo goed",
                         combine_word(first, second))


if __name__ == '__main__':
    unittest.main()
