"""
Imports
"""
import unittest

from client_package import view
from report_tree.report_node import ReportNode
from report_tree.report_leaf import TextLeaf
from report_tree.report_leaf import LabelLeaf


class ModelTest(unittest.TestCase):

    def test_identifier_function(self):
        node_1_label = 'mass'
        node_2_label = 'positive_finding'
        node_3_label = 'negative_finding'
        root_label = 'root'

        report_node_1 = ReportNode(node_1_label, [])
        report_node_2 = ReportNode(node_2_label, [report_node_1])
        report_node_3 = ReportNode(node_1_label, [])
        report_node_4 = ReportNode(node_2_label, [report_node_3])
        report_node_5 = ReportNode(node_1_label, [])
        report_node_6 = ReportNode(node_3_label, [report_node_5])
        report_node_7 = ReportNode(node_1_label, [])
        report_node_8 = ReportNode(node_3_label, [report_node_7])
        root = ReportNode(root_label, [report_node_2, report_node_4, report_node_6, report_node_8])
        json_tree = view.generate_tree(root, {})

        # pos_fin
        self.assertEqual(json_tree[1]["nodeId"], "_".join([node_2_label, root_label]))
        self.assertEqual(json_tree[1]["parentNodeId"], root_label)

        # mass_pos_fin
        self.assertEqual(json_tree[2]["nodeId"], "_".join([node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[2]["parentNodeId"], "_".join([node_2_label, root_label]))

        # pos_fin duplicate
        self.assertEqual(json_tree[3]["nodeId"], "_".join([node_2_label, root_label]) + "2")
        self.assertEqual(json_tree[3]["parentNodeId"], root_label)

        # mass_pos_fin duplicate
        self.assertEqual(json_tree[4]["nodeId"], "_".join([node_1_label, node_2_label, root_label]) + "2")
        self.assertEqual(json_tree[4]["parentNodeId"], "_".join([node_2_label, root_label]) + "2")

        # neg_fin
        self.assertEqual(json_tree[5]["nodeId"], "_".join([node_3_label, root_label]))
        self.assertEqual(json_tree[5]["parentNodeId"], root_label)

        # mass_neg_fin
        self.assertEqual(json_tree[6]["nodeId"], "_".join([node_1_label, node_3_label, root_label]))
        self.assertEqual(json_tree[6]["parentNodeId"], "_".join([node_3_label, root_label]))

        # neg_fin duplicate
        self.assertEqual(json_tree[7]["nodeId"], "_".join([node_3_label, root_label]) + "2")
        self.assertEqual(json_tree[7]["parentNodeId"], root_label)

        # mass_neg_fin duplicate
        self.assertEqual(json_tree[8]["nodeId"], "_".join([node_1_label, node_3_label, root_label]) + "2")
        self.assertEqual(json_tree[8]["parentNodeId"], "_".join([node_3_label, root_label]) + "2")
