"""
Imports
"""
import unittest

from client_package.model import Model
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
        model.create_identifiers(root)

        # test if no duplicates
        identifiers = model.tree_identifiers.values()
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_set_change_function(self):
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

        change1 = 'changed_label1'
        change2 = 'changed_label2'

        report_leaf_a = LabelLeaf(leaf_a_field, set(), leaf_a_field_confidence, leaf_a_label,
                                  (leaf_a_label, leaf_a_label_confidence))
        report_leaf_b = TextLeaf(leaf_b_field, leaf_b_field_confidence, leaf_b_text)
        spec_leaf_c = TextLeaf(spec_c_field)
        report_node_1 = ReportNode(node_1_label, [report_leaf_a, report_leaf_b, spec_leaf_c])
        report_node_2 = ReportNode(node_2_label, [report_node_1])
        root = ReportNode(root_label, [report_node_2])
        model.create_identifiers(root)
        json_tree = view.generate_tree(root, model.tree_identifiers, {})
        model.tree = root

        # Test leaf label change
        model.set_change(json_tree[4]['nodeId'], 'label', change1)
        self.assertEqual(change1, model.tree_changes[json_tree[4]['nodeId']].label)

        # Test leaf warning change
        model.set_change(json_tree[4]['nodeId'], 'warning', True)
        self.assertEqual(True, model.tree_changes[json_tree[4]['nodeId']].warning)
        model.set_change(json_tree[4]['nodeId'], 'warning', False)
        self.assertEqual(False, model.tree_changes[json_tree[4]['nodeId']].warning)

        # Test node category change
        model.set_change(json_tree[0]['nodeId'], 'label', change2)
        self.assertEqual(change2, model.tree_changes[json_tree[0]['nodeId']].label)
