"""
Imports
"""

import unittest
from src.report_node import ReportNode


class ReportNodeTest(unittest.TestCase):
    def test_init(self):
        child = ReportNode("labelchild", [], [])
        node = ReportNode("label", [child], ["Mass"])
        self.assertEqual(node.label, "label")
        self.assertEqual(node.children[0], child)
        self.assertEqual(node.expects, ["Mass"])

    def test_get_child(self):
        child0 = ReportNode("labelchild0", [], [])
        child1 = ReportNode("labelchild1", [], [])
        node = ReportNode("label", [child0, child1], ["Mass"])
        self.assertEqual(node.get_child(0), child0)
        self.assertEqual(node.get_child(1), child1)

    def test_addchild(self):
        child0 = ReportNode("labelchild0", [], [])
        child1 = ReportNode("labelchild1", [], [])
        node = ReportNode("label", [], ["Mass"])
        node.add_child(child0)
        node.add_child(child1)
        self.assertEqual(node.get_child(0), child0)
        self.assertEqual(node.get_child(1), child1)
