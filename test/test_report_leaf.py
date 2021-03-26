"""
Imports
"""

import unittest
from report_tree.report_leaf import LabelLeaf, TextLeaf


class ReportLeafTest(unittest.TestCase):
    def test_init(self):
        text = "value"
        field = "field"
        conf = .5
        labels = {"label1", "label2", "label3"}
        hint = "hint"
        pair = ("label2", .7)
        leaf = LabelLeaf(field, labels, field_conf=conf, text=text, label_pair=pair, hint=hint)
        self.assertEqual(leaf.field, field)
        self.assertEqual(leaf.labels, labels)
        self.assertEqual(leaf.hint, hint)

    def test_eq(self):
        leaf1 = TextLeaf("field1", .7, "text1", "hint1")
        leaf1a = TextLeaf("field1", .7, "text1", "hint2")
        leaf2 = TextLeaf("field2", .8, "text2", "hint3")
        self.assertTrue(leaf1 == leaf1a)
        self.assertTrue(leaf2 == leaf2)
        self.assertFalse(leaf1 == leaf2)

        leaf = LabelLeaf("field",  {"one", "other"}, .7, "text", ("label", .8), "hint")
        other = LabelLeaf("field", {"one", "other"}, .7, "text", ("label", .8), "hint")
        self.assertEqual(leaf, other)
        other = LabelLeaf("other", {"one", "other"}, 7, "text", ("label", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", {"one", "other"}, .8, "text", ("label", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", {"one", "other"}, .7, "other", ("label", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", {"two", "other"}, .7, "text", ("label", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", {"other", "one"}, .7, "text", ("label", .8), "hint")
        self.assertEqual(leaf, other, "Labels in different orders should be the same")
        other = LabelLeaf("field", {"one", "other"}, .7, "text", ("other", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", {"one", "other"}, .7, "text", ("label", .7), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", {"one", "other"}, .7, "text", ("label", .8), "other")
        self.assertEqual(leaf, other)

    def test_instance(self):
        text = TextLeaf("field", .7, "text", "hint")
        label = LabelLeaf("field", {"one", "other"}, .7, "text", ("label", .8), "hint")
        self.assertIsInstance(text, TextLeaf)
        self.assertNotIsInstance(text, LabelLeaf)
        self.assertIsInstance(label, LabelLeaf)
        self.assertIsInstance(label, TextLeaf)
