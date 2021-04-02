"""
imports
"""

import unittest

from reporttree.label_node import LabelNode
from reporttree.node import Node
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
        tree = Node('a', children=[
            Node('b', children=[Node('c', ("nested", 100)), Node('d', ("attribute", 100))]),
            Node('e', ("too", 100))
        ])

        hinter.hint(tree)

        self.assertEqual(3, len(tree.children), "make sure the missing LabelNode is added")
        self.assertIsInstance(tree.children[2], LabelNode)
        self.assertEqual(labels['f'], tree.children[2].options)

        self.assertIsNone(tree.children[0].children[0].hint)
        self.assertIsNone(tree.children[0].children[1].hint)
        self.assertEqual("hint", tree.children[1].hint)


if __name__ == '__main__':
    unittest.main()
