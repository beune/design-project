"""
Imports
"""

import unittest
from client_package import view

from client_package.model import Model

from reporttree.label_node import LabelNode
from reporttree.node import Node
from client_package.tree_changes import BackChange, FrontChange


class ViewTest(unittest.TestCase):

    def test_build_json_tree(self):
        model = Model(view)
        leaf_a_label = 'stervormige'
        leaf_a_label_confidence = 70
        leaf_a_field = 'margin'
        leaf_a_field_confidence = 55
        leaf_b_text = 'laterale bovenkwadrant linkermamma'
        leaf_b_field = 'location'
        leaf_b_field_confidence = 92
        spec_c_field = 'shape'
        node_1_label = 'mass'
        node_2_label = 'positive_finding'
        root_label = 'root'

        report_leaf_a = LabelNode(leaf_a_field, [], (leaf_a_label, leaf_a_field_confidence),
                                  (leaf_a_label, leaf_a_label_confidence))
        report_leaf_b = Node(leaf_b_field, (leaf_b_text, leaf_b_field_confidence))
        spec_leaf_c = Node(spec_c_field)
        report_node_1 = Node(node_1_label, children=[report_leaf_a, report_leaf_b, spec_leaf_c])
        report_node_2 = Node(node_2_label, children=[report_node_1])
        root = Node(root_label, children=[report_node_2])
        model.tree = root
        model.create_identifiers(root)
        json_tree = view.generate_tree(model)

        # test root
        self.assertEqual(json_tree[0]["parentNodeId"], None)
        self.assertEqual(json_tree[0]["template"], "<div class=\"domStyle\"><span>root</span></div>")
        self.assertEqual(json_tree[0]["text"], root_label)

        # test finding
        self.assertEqual(json_tree[1]["parentNodeId"], root_label)
        self.assertEqual(json_tree[1]["text"], node_2_label)

        # test category (mass)
        self.assertEqual(json_tree[2]["parentNodeId"], node_2_label)
        self.assertEqual(json_tree[2]["text"], node_1_label)

        # test labelLeaf field
        self.assertEqual(json_tree[3]["parentNodeId"], node_1_label)
        self.assertEqual(json_tree[3]["text"], leaf_a_field)

        # test labelLeaf label with low confidence
        self.assertEqual(json_tree[4]["parentNodeId"], leaf_a_field)
        self.assertEqual(json_tree[4]["lowConfidence"], True)
        self.assertEqual(json_tree[4]["text"], leaf_a_label)

        # test textLeaf field
        self.assertEqual(json_tree[5]["parentNodeId"], node_1_label)
        self.assertEqual(json_tree[5]["text"], leaf_b_field)

        # test textLeaf text
        self.assertEqual(json_tree[6]["parentNodeId"], leaf_b_field)
        self.assertEqual(json_tree[6]["text"], leaf_b_text)

        # test spec_leaf
        self.assertEqual(json_tree[7]["parentNodeId"], node_1_label)
        self.assertEqual(json_tree[7]["speculative"], True)
        self.assertEqual(json_tree[7]["text"], spec_c_field)

    def test_apply_changes(self):
        model = Model(view)
        leaf_a_label = 'stervormige'
        leaf_a_field = 'margin'

        report_leaf_a = LabelNode(leaf_a_field, [], (leaf_a_label, 55), (leaf_a_label, 55))
        report_node_1 = Node('mass', children=[report_leaf_a])
        report_node_2 = Node('positive_finding', children=[report_node_1])
        root = Node('root', children=[report_node_2])
        model.tree = root
        model.create_identifiers(root)
        json_tree = view.generate_tree(model)

        # Test label change
        self.assertEqual(json_tree[4]["text"], leaf_a_label)  # pre change
        leaf_a_id = json_tree[3]["nodeId"]
        leaf_a_new_label = "circumscribed"
        model.set_back_change(leaf_a_id, leaf_a_new_label)
        model.apply_back_changes()
        json_tree = view.generate_tree(model)
        self.assertEqual(json_tree[4]["text"], leaf_a_new_label)  # post change

        # Test ignore warning
        self.assertEqual(json_tree[3]["lowConfidence"], True)  # pre change
        self.assertEqual(json_tree[4]["lowConfidence"], True)
        label_a_id = json_tree[3]["nodeId"]
        leaf_a_id = json_tree[4]["nodeId"]
        model.set_front_change(label_a_id, False)
        json_tree = view.generate_tree(model)
        self.assertEqual(json_tree[3]["lowConfidence"], False)
        model.set_front_change(leaf_a_id, False)
        json_tree = view.generate_tree(model)
        self.assertEqual(json_tree[4]["lowConfidence"], False)
