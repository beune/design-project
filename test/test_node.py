"""
Imports
"""

import unittest

from reporttree.node import Node


class NodeTest(unittest.TestCase):
    def test_init(self):
        child = Node("child")
        node = Node("category", children=[child])
        self.assertEqual(node.category, "category")
        self.assertEqual(node.children[0], child)

    def test_add_child(self):
        child0 = Node("child0")
        child1 = Node("child1")
        node = Node("label")
        node.add_child(child0)
        node.add_child(child1)
        self.assertEqual(node.children[0], child0)
        self.assertEqual(node.children[1], child1)

    def test_text(self):
        node = Node("category")
        self.assertIsNone(node.text)
        node = Node("category", ("This is text", 60))
        self.assertEqual(node.text, "This is text")
        node.corr_text = "Text is corrected"
        self.assertEqual(node.text, "Text is corrected")
