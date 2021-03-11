"""
imports
"""

import unittest

from src.report_leaf import ReportLeaf
from src.report_node import ReportNode
from src.server.hinter import Hinter


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
            ReportNode('b', [ReportLeaf("nested", 'c', 1), ReportLeaf("attribute", 'd', 1)]),
            ReportLeaf("too", 'e', 1)
        ])

        hinter.hint(tree)
        self.assertEqual("hint", tree.get_child(1).hint)
        self.assertEqual(['b', 'e', 'f'], tree.expects)
        self.assertEqual(tree.get_child(0).expects, [])
        self.assertIsNone(tree.get_child(0).get_child(0).hint)


if __name__ == '__main__':
    unittest.main()
