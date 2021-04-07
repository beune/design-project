"""
Imports
"""

import unittest

from reporttree.label_node import LabelNode
from reporttree.node import Node


class LabelNodeTest(unittest.TestCase):
    def test_init(self):
        path = ["category"]
        options = ["label1", "label2", "label3"]
        hint = "hint"
        text_pair = ("this value", 50)
        label_pair = ("label2", 70)
        leaf = LabelNode(path, options, text_prediction=text_pair, label_prediction=label_pair, hint=hint)
        self.assertEqual(leaf.category, "category")
        self.assertEqual(leaf.options, options)
        self.assertEqual(leaf.hint, hint)

    def test_eq(self):
        leaf1 = Node(["field1"], text_prediction=("text1", 70), hint="hint1")
        leaf1a = Node(["field1"], text_prediction=("text1", 70), hint="hint2")
        leaf2 = Node(["field2"], text_prediction=("text1", 70), hint="hint3")
        self.assertEqual(leaf1, leaf1a)
        self.assertEqual(leaf2, leaf2)
        self.assertNotEqual(leaf1, leaf2)

        leaf = LabelNode(["field"],  ["one", "other"], ("text", 70), ("label", 80), hint="hint")
        other = LabelNode(["field"], ["one", "other"], ("text", 70), ("label", 80), hint="hint")
        self.assertEqual(leaf, other)
        other = LabelNode(["other"], ["one", "other"], ("text", 70), ("label", 80), hint="hint")
        self.assertNotEqual(leaf, other)
        other = LabelNode(["field"], ["one", "other"], ("text", 80), ("label", 80), hint="hint")
        self.assertEqual(leaf, other)
        other = LabelNode(["field"], ["one", "other"], ("other", 70), ("label", 80), hint="hint")
        self.assertNotEqual(leaf, other)
        other = LabelNode(["field"], ["two", "other"], ("text", 70), ("label", 80), hint="hint")
        self.assertNotEqual(leaf, other)
        other = LabelNode(["field"], ["other", "one"], ("text", 70), ("label", 80), hint="hint")
        self.assertNotEqual(leaf, other, "Options in different orders shouldn't be the same")
        other = LabelNode(["field"], ["one", "other"], ("text", 70), ("other", 80), hint="hint")
        self.assertNotEqual(leaf, other)
        other = LabelNode(["field"], ["one", "other"], ("text", 70), ("label", 70), hint="hint")
        self.assertEqual(leaf, other)
        other = LabelNode(["field"], ["one", "other"], ("text", 70), ("label", 80), hint="other")
        self.assertEqual(leaf, other)

    def test_instance(self):
        text = Node(["field"], ("text", 70), hint="hint")
        label = LabelNode(["field"], ["one", "other"], ("text", 70), ("label", 80), hint="hint")
        self.assertIsInstance(text, Node)
        self.assertNotIsInstance(text, LabelNode)
        self.assertIsInstance(label, LabelNode)
        self.assertIsInstance(label, Node)
