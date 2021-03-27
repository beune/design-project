"""
Imports
"""

import unittest
from client import view
from client import controller
from client import model

from report_tree.report_node import ReportNode
from report_tree.report_leaf import ReportLeaf


class ViewTest(unittest.TestCase):
    def test_build_json_tree(self):
        report_leaf_a = ReportLeaf('stervormige', 'margin', 0.55,
                                   {'stervormige': 55, 'circumscribed': 0, 'obscured': 0})
        report_node_1 = ReportNode('mass', [report_leaf_a], ['shape', 'margin', 'density'])
        report_node_2 = ReportNode('positive_finding', [report_node_1], [])
        root = ReportNode('root', [report_node_2], [])
        json_tree = view.generate_tree(root)

        self.assertEqual(json_tree[0]["nodeId"], "root")
        self.assertEqual(json_tree[0]["parentNodeId"], None)

    def test_identifier_function(self):
        field = 'margin'
        text = 'stervormige'
        leaf = ReportLeaf(field, text, 0.55,
                          {'stervormige': 55, 'circumscribed': 0, 'obscured': 0})
        root = ReportNode('root', [leaf], [])
        json_leaf = view.generate_tree(root)

        self.assertEqual(json_leaf[1]["nodeId"], field + 'root')
        self.assertEqual(json_leaf[2]["nodeId"], text + 'root')

    def test_apply_changes(self):
        leaf_value = 'stervormige'
        report_leaf_a = ReportLeaf(leaf_value, 'margin', 0.55,
                                   {'stervormige': 55, 'circumscribed': 0, 'obscured': 0})
        report_node_1 = ReportNode('mass', [report_leaf_a], ['shape', 'margin', 'density'])
        report_node_2 = ReportNode('positive_finding', [report_node_1], [])
        root = ReportNode('root', [report_node_2], [])
        json_tree = view.generate_tree(root)

        self.assertEqual(json_tree[4]["label"], leaf_value)
        leaf_id = json_tree[4]["nodeId"]
        leaf_changed_value = "circumscribed"
        json_tree = view.generate_tree(root, {leaf_id: leaf_changed_value})
        self.assertEqual(json_tree[4]["label"], leaf_changed_value)
