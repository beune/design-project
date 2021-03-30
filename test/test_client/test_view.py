"""
Imports
"""

import unittest
from client import view

from report_tree.report_node import ReportNode
from report_tree.report_leaf import TextLeaf
from report_tree.report_leaf import LabelLeaf


class ViewTest(unittest.TestCase):

    def test_build_json_tree(self):
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
        json_tree = view.generate_tree(root, {})

        # test root
        self.assertEqual(json_tree[0]["nodeId"], root_label)
        self.assertEqual(json_tree[0]["parentNodeId"], None)
        self.assertEqual(json_tree[0]["valueNode"], False)
        self.assertEqual(json_tree[0]["template"], "<div class=\"domStyle\"><span>root</span></div>")
        self.assertEqual(json_tree[0]["label"], root_label)

        # test finding
        self.assertEqual(json_tree[1]["nodeId"], "_".join([node_2_label, root_label]))
        self.assertEqual(json_tree[1]["parentNodeId"], root_label)
        self.assertEqual(json_tree[1]["label"], node_2_label)

        # test category (mass)
        self.assertEqual(json_tree[2]["nodeId"], "_".join([node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[2]["parentNodeId"], "_".join([node_2_label, root_label]))
        self.assertEqual(json_tree[2]["valueNode"], False)
        self.assertEqual(json_tree[2]["label"], node_1_label)

        # test labelLeaf field
        self.assertEqual(json_tree[3]["nodeId"], "_".join([leaf_a_field, node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[3]["parentNodeId"], "_".join([node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[3]["valueNode"], False)
        self.assertEqual(json_tree[3]["label"], leaf_a_field)

        # test labelLeaf label with low confidence
        self.assertEqual(json_tree[4]["nodeId"], "_".join([leaf_a_label, leaf_a_field, node_1_label, node_2_label,
                                                           root_label]))
        self.assertEqual(json_tree[4]["parentNodeId"], "_".join([leaf_a_field, node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[4]["valueNode"], True)
        self.assertEqual(json_tree[4]["lowConfidence"], True)
        self.assertEqual(json_tree[4]["label"], leaf_a_label)

        # test textLeaf field
        self.assertEqual(json_tree[5]["nodeId"], "_".join([leaf_b_field, node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[5]["parentNodeId"], "_".join([node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[5]["label"], leaf_b_field)

        # test textLeaf text
        self.assertEqual(json_tree[6]["nodeId"], "_".join([leaf_b_text, leaf_b_field, node_1_label, node_2_label,
                                                           root_label]))
        self.assertEqual(json_tree[6]["parentNodeId"], "_".join([leaf_b_field, node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[6]["valueNode"], True)
        self.assertEqual(json_tree[6]["label"], leaf_b_text)

        # test spec_leaf
        self.assertEqual(json_tree[7]["nodeId"], "_".join([spec_c_field, node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[7]["parentNodeId"], "_".join([node_1_label, node_2_label, root_label]))
        self.assertEqual(json_tree[7]["speculative"], True)
        self.assertEqual(json_tree[7]["label"], spec_c_field)

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

    def test_apply_changes(self):
        leaf_a_label = 'stervormige'
        leaf_a_field = 'margin'

        report_leaf_a = LabelLeaf(leaf_a_field, set(), 0.55, leaf_a_label,
                                  (leaf_a_label, 80))
        report_node_1 = ReportNode('mass', [report_leaf_a])
        report_node_2 = ReportNode('positive_finding', [report_node_1])
        root = ReportNode('root', [report_node_2])
        json_tree = view.generate_tree(root, {})

        # test pre change
        self.assertEqual(json_tree[4]["nodeId"], "_".join([leaf_a_label, leaf_a_field, "mass_positive_finding_root"]))
        self.assertEqual(json_tree[4]["parentNodeId"], "_".join([leaf_a_field, "mass_positive_finding_root"]))
        self.assertEqual(json_tree[4]["label"], leaf_a_label)

        leaf_a_id = json_tree[4]["nodeId"]
        leaf_a_new_label = "circumscribed"
        json_tree = view.generate_tree(root, {leaf_a_id: leaf_a_new_label})

        # test after change
        self.assertEqual(json_tree[4]["nodeId"], "_".join([leaf_a_label, leaf_a_field, "mass_positive_finding_root"]))
        self.assertEqual(json_tree[4]["parentNodeId"], "_".join([leaf_a_field, "mass_positive_finding_root"]))
        self.assertEqual(json_tree[4]["label"], leaf_a_new_label)

    def test_build_tree_from_json(self):
        root_category = 'kaas'
        leaf_field = 'kaaas'
        leaf_value = 'kas'
        leaf_text = 'käs'
        leaf_hint = 'kissoe'
        leaf_field_conf = 0.23
        leaf_label_conf = 0.2190
        leaf_alternatives = ['niffo', 'bro', 'niffobro']
        json_tree = [{'nodeId': 'mass_positive_finding_root', 'parentNodeId': None, 'valueNode': False,
                      'lowConfidence': False, 'width': 347, 'height': 147,
                      'template': '<div class="domStyle"><span>mass</span></div>', 'alternatives': None,
                      'originalTemplate': '<div class="domStyle"><span>mass</span></div>', 'hint': None, 'text': 'mass',
                      'speculative': False, 'label': root_category, 'isLabel': False, 'confidence': None,
                      'directSubordinates': 5,
                      'totalSubordinates': 10},
                     {'nodeId': 'margin_mass_positive_finding_root', 'parentNodeId': 'mass_positive_finding_root',
                      'valueNode': False, 'lowConfidence': True, 'width': 347, 'height': 147,
                      'template': '<div class="domStyle"><span>margin</span></div><span class="confidence">55%</span>',
                      'alternatives': None,
                      'originalTemplate': '<div class="domStyle"><span>margin</span></div><span class="confidence">55%</span>',
                      'hint': leaf_hint,
                      'text': 'margin', 'speculative': False, 'label': leaf_field, 'isLabel': False,
                      'confidence': leaf_field_conf, 'directSubordinates': 1, 'totalSubordinates': 1},
                     {'nodeId': 'stervormige_margin_mass_positive_finding_root',
                      'parentNodeId': 'margin_mass_positive_finding_root', 'valueNode': True, 'lowConfidence': True,
                      'width': 347, 'height': 147,
                      'template': '<div class="domStyle"><span>obscured</div></span><span class="material-icons">mode</span>',
                      'alternatives': leaf_alternatives,
                      'originalTemplate': '<div class="domStyle"><span>stervormige</span></div><span class="confidence">70%</span>',
                      'hint': 'stervormige', 'text': leaf_text, 'speculative': False, 'label': leaf_value,
                      'isLabel': True,
                      'confidence': leaf_label_conf, 'directSubordinates': 0, 'totalSubordinates': 0}]

        tree_root = view.tree_from_json(json_tree, json_tree[0])[1]
        tree_leaf = tree_root.children[0]

        # test structure
        self.assertEqual(tree_root.category, root_category)
        self.assertEqual(tree_leaf.field, leaf_field)
        self.assertEqual(tree_leaf.label, leaf_value)
        self.assertEqual(tree_leaf.text, leaf_text)
        self.assertEqual(tree_leaf.hint, leaf_hint)
        self.assertEqual(tree_leaf.field_conf, leaf_field_conf)
        self.assertEqual(tree_leaf.label_conf, leaf_label_conf)
        self.assertEqual(tree_leaf.labels, leaf_alternatives)
