"""
Imports
"""

import unittest
from report_tree.report_leaf import LabelLeaf, ReportLeaf


class ReportLeafTest(unittest.TestCase):
    def test_init(self):
        text = "value"
        field = "field"
        conf = .5
        labels = {"label1", "label2", "label3"}
        hint = "hint"
        pair = ("label2", .7)
        leaf = LabelLeaf(field, conf, text, labels, pair, hint)
        self.assertEqual(leaf.field, field)
        self.assertEqual(leaf.labels, labels)
        self.assertEqual(leaf.hint, hint)

    def test_eq(self):
        leaf1 = ReportLeaf("field1", .7, "text1", "hint1")
        leaf1a = ReportLeaf("field1", .7, "text1", "hint2")
        leaf2 = ReportLeaf("field2", .8, "text2", "hint3")
        self.assertTrue(leaf1 == leaf1a)
        self.assertTrue(leaf2 == leaf2)
        self.assertFalse(leaf1 == leaf2)

        leaf = LabelLeaf("field", .7, "text", {"one", "other"}, ("label", .8), "hint")
        other = LabelLeaf("field", .7, "text", {"one", "other"}, ("label", .8), "hint")
        self.assertEqual(leaf, other)
        other = LabelLeaf("other", .7, "text", {"one", "other"}, ("label", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", .8, "text", {"one", "other"}, ("label", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", .7, "other", {"one", "other"}, ("label", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", .7, "text", {"two", "other"}, ("label", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", .7, "text", {"other", "one"}, ("label", .8), "hint")
        self.assertEqual(leaf, other, "Labels in different orders should be the same")
        other = LabelLeaf("field", .7, "text", {"one", "other"}, ("other", .8), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", .7, "text", {"one", "other"}, ("label", .7), "hint")
        self.assertNotEqual(leaf, other)
        other = LabelLeaf("field", .7, "text", {"one", "other"}, ("label", .8), "other")
        self.assertEqual(leaf, other)

    def test_instance(self):
        text = ReportLeaf("field", .7, "text", "hint")
        label = LabelLeaf("field", .7, "text", {"one", "other"}, ("label", .8), "hint")
        self.assertIsInstance(text, ReportLeaf)
        self.assertNotIsInstance(text, LabelLeaf)
        self.assertIsInstance(label, LabelLeaf)
        self.assertIsInstance(label, ReportLeaf)
