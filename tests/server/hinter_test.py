"""
imports
"""

import unittest

from src.report_leaf import ReportLeaf
from src.report_node import ReportNode
from src.server.hinter import Hinter


class MyTestCase(unittest.TestCase):
    def test_hint(self):
        # TODO: declarations naar setup?
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
        self.assertEqual("hint", tree.children[1].hint)  # TODO: misschien een mooiere getter op nodes?
        self.assertEqual(['b', 'e', 'f'], tree.expects)
        self.assertIsNone(tree.children[0].expects)  # TODO: is None hier mooi? of liever een lege list?
        self.assertIsNone(tree.children[0].children[0].hint)  # TODO: is None hier mooi? of liever een lege string?


if __name__ == '__main__':
    unittest.main()
