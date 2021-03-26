"""
imports
"""

import unittest

from report_tree.report_leaf import ReportLeaf
from report_tree.report_node import ReportNode
from servpackage.hinter import Hinter


class MyTestCase(unittest.TestCase):
    def test_hint(self):
        expected = {
            'a': ['b', 'e', 'f']
        }

        hints = {
            'e': "hint"
        }
        hinter = Hinter(expected, hints)
        tree = ReportNode('a', [
            ReportNode('b', [ReportLeaf('c', 1, "nested"), ReportLeaf('d', 1, "attribute")]),
            ReportLeaf('e', 1, "too")
        ])

        hinter.hint(tree)
        self.assertEqual("hint", tree.get_child(1).hint)
        self.assertEqual(['b', 'e', 'f'], tree.expects)
        self.assertEqual(tree.get_child(0).expects, [])
        self.assertIsNone(tree.get_child(0).get_child(0).hint)


if __name__ == '__main__':
    unittest.main()
