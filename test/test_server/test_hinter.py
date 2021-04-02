"""
imports
"""

import unittest

from reporttree.report_leaf import TextLeaf, LabelLeaf
from reporttree.report_node import ReportNode
from server_package.hinter import Hinter


class MyTestCase(unittest.TestCase):
    def test_hint(self):
        expected = {
            # 'a': ['b', 'e', 'f'] ReportNodes are not checked, only ReportLeaves
            'a': ['e', 'f']
        }
        labels = {
            'f': {'l1', 'l2', 'l3'}
        }
        hints = {
            'e': "hint"
        }
        hinter = Hinter(expected, labels, hints)
        tree = ReportNode('a', [
            ReportNode('b', [TextLeaf('c', 1, "nested"), TextLeaf('d', 1, "attribute")]),
            TextLeaf('e', 1, "too")
        ])

        hinter.hint(tree)

        self.assertEqual(3, len(tree.children), "make sure the missing LabelLeaf is added")
        self.assertIsInstance(tree.get_child(2), LabelLeaf)
        self.assertEqual(labels['f'], tree.get_child(2).labels)

        self.assertIsNone(tree.get_child(0).get_child(0).hint)
        self.assertIsNone(tree.get_child(0).get_child(1).hint)
        self.assertEqual("hint", tree.get_child(1).hint)


if __name__ == '__main__':
    unittest.main()
