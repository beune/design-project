"""
Imports
"""

import unittest
from reporttree.report_node import ReportNode


class ReportNodeTest(unittest.TestCase):
    def test_init(self):
        child = ReportNode("labelchild", [])
        node = ReportNode("category", [child])
        self.assertEqual(node.category, "category")
        self.assertEqual(node.children[0], child)

    def test_get_child(self):
        child0 = ReportNode("labelchild0", [])
        child1 = ReportNode("labelchild1", [])
        node = ReportNode("label", [child0, child1])
        self.assertEqual(node.get_child(0), child0)
        self.assertEqual(node.get_child(1), child1)

    def test_add_child(self):
        child0 = ReportNode("labelchild0", [])
        child1 = ReportNode("labelchild1", [])
        node = ReportNode("label", [])
        node.add_child(child0)
        node.add_child(child1)
        self.assertEqual(node.get_child(0), child0)
        self.assertEqual(node.get_child(1), child1)
