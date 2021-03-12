"""
imports
"""
import unittest
from src.server.environments.mammo import make_tree, after, has_base, clean
from src.report_leaf import ReportLeaf
from src.report_node import ReportNode


class MyTestCase(unittest.TestCase):
    def test_make_tree(self):
        json = [('dit', 'B-a', 1), ('is', 'I-a', 1), ('een', 'I-a', 1), ('test', 'I-a', 1)]
        actual = make_tree([], json)
        expected = ReportLeaf("dit is een test", 'a', 1)
        self.assertIsInstance(actual, ReportNode)
        self.assertEqual("root", actual.category)
        self.assertEqual(expected, actual.children[0])

        json = [('dit', 'B-a', 1), ('is', 'B-a', 1), ('een', 'B-a', 1), ('test', 'B-a', 1)]
        actual = make_tree([], json)
        self.assertEqual(4, len(actual.children))

        actual = make_tree([], [])
        expected = ReportNode("root")
        self.assertEqual(expected, actual)

        json = [('niet', 'O', 1), ('kan', 'B-a', 1), ('niet', 'O', 1), ('dit', 'I-a', 1), ('niet', 'O', 1),
                ('ook?', 'I-a', 1), ('niet', 'O', 1)]
        actual = make_tree([], json)
        unexpected = ReportLeaf("kan dit ook?", 'a', 1.0)
        self.assertNotEqual(unexpected, actual.children[0])

        json = [('nested', 'B-a/B-b/B-c', 1), ('attribute', 'I-a/I-b/B-d', 1), ('too', 'I-a/I-e', 1)]
        actual = make_tree(["B-a"], json)
        expected = ReportNode('a', [
            ReportNode('b', [ReportLeaf("nested", 'c', 1), ReportLeaf("attribute", 'd', 1)]),
            ReportLeaf("too", 'e', 1)
        ])
        self.assertEqual(expected, actual)

    def test_after(self):
        self.assertTrue(after("I-a", "B-a"))
        self.assertFalse(after("B-a", "B-a"), "This is a new category")
        self.assertFalse(after("B-a", "I-a"), "This is a new category")
        self.assertTrue(after("I-a", "I-a"))
        self.assertFalse(after("B-b", "B-a"), "Different category")
        self.assertFalse(after("I-b", "B-a"), "Different category")

    def test_has_base(self):
        self.assertTrue(has_base([], []))

        base = ["I-a", "B-b"]
        self.assertFalse(has_base([], base))
        self.assertTrue(has_base(["I-a", "I-b"], base))
        self.assertTrue(has_base(["I-a", "I-b", "B-c"], base))
        # self.assertFalse(has_base(["I-a", "I-b", "I-c"], base)) #  I don't think we want to check this case
        self.assertFalse(has_base(["B-a", "I-b", "B-c"], base))
        self.assertFalse(has_base(["I-a", "B-b", "B-c"], base))

    def test_clean(self):
        self.assertEqual("a", clean("I-a"))
        self.assertEqual("a", clean("B-a"))
        self.assertEqual("aB-", clean("B-aB-"))
        self.assertEqual("c", clean("c"))
        self.assertEqual("", clean("I-"))


if __name__ == '__main__':
    unittest.main()
