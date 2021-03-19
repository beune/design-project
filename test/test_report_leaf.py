"""
Imports
"""

import unittest
from report_tree.report_leaf import ReportLeaf


class ReportLeafTest(unittest.TestCase):
    def test_init(self):
        text = "value"
        key = "key"
        conf = .5
        labels = {"label": 0.85}
        hint = "hint"
        leaf = ReportLeaf(text, key, conf, labels, hint)
        self.assertEqual(leaf.field, key)
        self.assertEqual(leaf.labels, labels)
        self.assertEqual(leaf.hint, hint)

    def test_eq(self):
        leaf1 = ReportLeaf("key1", "text1", .7, {"label1": 0.5}, "hint1")
        leaf1a = ReportLeaf("key1", "text1", .7, {"label1": 0.5}, "hint1")
        leaf2 = ReportLeaf("key2", "text2", .8, {"label2": 0.6}, "hint2")
        self.assertTrue(leaf1 == leaf1a)
        self.assertTrue(leaf2 == leaf2)
        self.assertFalse(leaf1 == leaf2)
