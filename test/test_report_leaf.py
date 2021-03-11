"""
Imports
"""

import unittest
from src.report_leaf import ReportLeaf


class ReportLeafTest(unittest.TestCase):
    def test_init(self):
        text = "value"
        label = "label"
        certainty = 0.85
        hint = "hint"
        leaf = ReportLeaf(label, {text: certainty}, hint)
        self.assertEqual(leaf.label, label)
        self.assertEqual(leaf.values, {text: certainty})
        self.assertEqual(leaf.hint, hint)

    def test_eq(self):
        leaf1 = ReportLeaf("text1", {"label1": 0.5}, "hint1")
        leaf1a = ReportLeaf("text1", {"label1": 0.5}, "hint1")
        leaf2 = ReportLeaf("text2", {"label2": 0.6}, "hint2")
        self.assertTrue(leaf1 == leaf1a)
        self.assertTrue(leaf2 == leaf2)
        self.assertFalse(leaf1 == leaf2)
