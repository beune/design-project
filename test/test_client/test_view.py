"""
Imports
"""

import unittest
from client_package import view

from client_package.model import Model
from report_tree.report_node import ReportNode
from report_tree.report_leaf import TextLeaf
from report_tree.report_leaf import LabelLeaf

from client_package.tree_changes import Change


class ViewTest(unittest.TestCase):

    def test_build_json_tree(self):
        model = Model(view.initialize, view.update, view.server_error, view.show_loader)
        leaf_a_label = 'stervormige'
        leaf_a_label_confidence = 0.70
        leaf_a_field = 'margin'
        leaf_a_field_confidence = 0.55
        leaf_b_text = 'laterale bovenkwadrant linkermamma'
        leaf_b_field = 'location'
        leaf_b_field_confidence = 0.92
        spec_c_field = 'shape'
        node_1_label = 'mass'
        node_2_label = 'positive_finding'
        root_label = 'root'

        report_leaf_a = LabelLeaf(leaf_a_field, set(), leaf_a_field_confidence, leaf_a_label,
                                  (leaf_a_label, leaf_a_label_confidence))
        report_leaf_b = TextLeaf(leaf_b_field, leaf_b_field_confidence, leaf_b_text)
        spec_leaf_c = TextLeaf(spec_c_field)
        report_node_1 = ReportNode(node_1_label, [report_leaf_a, report_leaf_b, spec_leaf_c])
        report_node_2 = ReportNode(node_2_label, [report_node_1])
        root = ReportNode(root_label, [report_node_2])
        model.create_identifiers(root)
        json_tree = view.generate_tree(root, model.tree_identifiers, {})

        # test root
        self.assertEqual(json_tree[0]["parentNodeId"], None)
        self.assertEqual(json_tree[0]["valueNode"], False)
        self.assertEqual(json_tree[0]["template"], "<div class=\"domStyle\"><span>root</span></div>")
        self.assertEqual(json_tree[0]["label"], root_label)

        # test finding
        self.assertEqual(json_tree[1]["parentNodeId"], root_label)
        self.assertEqual(json_tree[1]["label"], node_2_label)

        # test category (mass)
        self.assertEqual(json_tree[2]["parentNodeId"], node_2_label)
        self.assertEqual(json_tree[2]["valueNode"], False)
        self.assertEqual(json_tree[2]["label"], node_1_label)

        # test labelLeaf field
        self.assertEqual(json_tree[3]["parentNodeId"], node_1_label)
        self.assertEqual(json_tree[3]["valueNode"], False)
        self.assertEqual(json_tree[3]["label"], leaf_a_field)

        # test labelLeaf label with low confidence
        self.assertEqual(json_tree[4]["parentNodeId"], leaf_a_field)
        self.assertEqual(json_tree[4]["valueNode"], True)
        self.assertEqual(json_tree[4]["lowConfidence"], True)
        self.assertEqual(json_tree[4]["label"], leaf_a_label)

        # test textLeaf field
        self.assertEqual(json_tree[5]["parentNodeId"], node_1_label)
        self.assertEqual(json_tree[5]["label"], leaf_b_field)

        # test textLeaf text
        self.assertEqual(json_tree[6]["parentNodeId"], leaf_b_field)
        self.assertEqual(json_tree[6]["valueNode"], True)
        self.assertEqual(json_tree[6]["label"], leaf_b_text)

        # test spec_leaf
        self.assertEqual(json_tree[7]["parentNodeId"], node_1_label)
        self.assertEqual(json_tree[7]["speculative"], True)
        self.assertEqual(json_tree[7]["label"], spec_c_field)

    def test_apply_changes(self):
        model = Model(view.initialize, view.update, view.server_error, view.show_loader)
        leaf_a_label = 'stervormige'
        leaf_a_field = 'margin'

        report_leaf_a = LabelLeaf(leaf_a_field, set(), 0.55, leaf_a_label,
                                  (leaf_a_label, 0.55))
        report_node_1 = ReportNode('mass', [report_leaf_a])
        report_node_2 = ReportNode('positive_finding', [report_node_1])
        root = ReportNode('root', [report_node_2])
        model.create_identifiers(root)
        json_tree = view.generate_tree(root, model.tree_identifiers, {})

        # Test label change
        self.assertEqual(json_tree[4]["label"], leaf_a_label)  # pre change
        leaf_a_id = json_tree[4]["nodeId"]
        leaf_a_new_label = "circumscribed"
        json_tree = view.generate_tree(root, model.tree_identifiers, {leaf_a_id: Change(label=leaf_a_new_label)})
        self.assertEqual(json_tree[4]["label"], leaf_a_new_label)  # post change

        # Test ignore warning
        self.assertEqual(json_tree[4]["lowConfidence"], True)  # pre change
        leaf_a_id = json_tree[4]["nodeId"]
        json_tree = view.generate_tree(root, model.tree_identifiers, {leaf_a_id: Change(warning=False)})
        self.assertEqual(json_tree[4]["lowConfidence"], False)  # post change
