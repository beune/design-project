"""
Imports
"""
import unittest

from client_package.model import Model
from client_package import view
from reporttree.node import Node
from reporttree.label_node import LabelNode


class ModelTest(unittest.TestCase):

    def test_identifier_function(self):
        model = Model(view.initialize, view.update, view.server_error, view.show_loader)
        node_1_label = 'mass'
        node_2_label = 'positive_finding'
        node_3_label = 'negative_finding'
        root_label = 'root'

        report_node_1 = Node(node_1_label, children=[])
        report_node_2 = Node(node_2_label, children=[report_node_1])
        report_node_3 = Node(node_1_label, children=[])
        report_node_4 = Node(node_2_label, children=[report_node_3])
        report_node_5 = Node(node_1_label, children=[])
        report_node_6 = Node(node_3_label, children=[report_node_5])
        report_node_7 = Node(node_1_label, children=[])
        report_node_8 = Node(node_3_label, children=[report_node_7])
        root = Node(root_label, children=[report_node_2, report_node_4, report_node_6, report_node_8])
        model.create_identifiers(root)

        # test if no duplicates
        identifiers = model.tree_identifiers.values()
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_set_change_function(self):
        model = Model(view.initialize, view.update, view.server_error, view.show_loader)

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

        change1 = 'changed_label1'
        change2 = 'changed_label2'

        report_leaf_a = LabelNode(leaf_a_field, [], (leaf_a_label, leaf_a_field_confidence),
                                  (leaf_a_label, leaf_a_label_confidence))
        report_leaf_b = Node(leaf_b_field, (leaf_b_text, leaf_b_field_confidence))
        spec_leaf_c = Node(spec_c_field)
        report_node_1 = Node(node_1_label, children=[report_leaf_a, report_leaf_b, spec_leaf_c])
        report_node_2 = Node(node_2_label, children=[report_node_1])
        root = Node(root_label, children=[report_node_2])
        model.create_identifiers(root)
        json_tree = view.generate_tree(model)
        model.tree = root

        # Test leaf label change
        model.set_back_change(json_tree[4]['nodeId'], change1)
        model.apply_back_changes()
        json_tree = view.generate_tree(model)
        self.assertEqual(change1, json_tree[4]['nodeId'].label)

        # Test node category change
        model.set_back_change(json_tree[0]['nodeId'], change2)
        model.apply_back_changes()
        json_tree = view.generate_tree(model)
        self.assertEqual(change2, json_tree[0]['nodeId'].label)
