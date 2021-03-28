"""
Imports
"""

import unittest
from client import view

from report_tree.report_node import ReportNode
from report_tree.report_leaf import ReportLeaf


class ViewTest(unittest.TestCase):
    def test_build_json_tree(self):
        leaf_a_label = 'stervormige'
        leaf_a_field = 'margin'
        leaf_b_label = 'laterale bovenkwadrant linkermamma'
        leaf_b_field = 'location'
        node_1_label = 'mass'
        node_2_label = 'positive_finding'
        root_label = 'root'

        report_leaf_a = ReportLeaf(leaf_a_label, leaf_a_field, 0.55,
                                   {'stervormige': 55, 'circumscribed': 0, 'obscured': 0})
        report_leaf_b = ReportLeaf(leaf_b_label, leaf_b_field, 0.92,
                                   None)
        report_node_1 = ReportNode(node_1_label, [report_leaf_a, report_leaf_b], ['shape', 'density', 'margin'])
        report_node_2 = ReportNode(node_2_label, [report_node_1], [])
        root = ReportNode(root_label, [report_node_2], [])
        json_tree = view.generate_tree(root)

        self.assertEqual(json_tree[0]["nodeId"], root_label)
        self.assertEqual(json_tree[0]["parentNodeId"], None)
        self.assertEqual(json_tree[0]["valueNode"], False)
        self.assertEqual(json_tree[0]["template"], "<div class=\"domStyle\"><span>root</span></div>")
        self.assertEqual(json_tree[0]["label"], "root")

        self.assertEqual(json_tree[1]["nodeId"], node_2_label + "_" + root_label)
        self.assertEqual(json_tree[1]["parentNodeId"], root_label)
        self.assertEqual(json_tree[1]["valueNode"], False)
        self.assertEqual(json_tree[1]["template"], "<div class=\"domStyle\"><span>positive_finding</span></div>")
        self.assertEqual(json_tree[1]["label"], node_2_label)

        self.assertEqual(json_tree[2]["nodeId"], node_1_label + "_" + node_2_label + "_" + root_label)
        self.assertEqual(json_tree[2]["parentNodeId"], node_2_label + "_" + root_label)
        self.assertEqual(json_tree[2]["valueNode"], False)
        self.assertEqual(json_tree[2]["template"], "<div class=\"domStyle\"><span>mass</span></div>")
        self.assertEqual(json_tree[2]["label"], node_1_label)

        self.assertEqual(json_tree[3]["nodeId"], "shape" + "_" + node_1_label + "_" + node_2_label + "_" + root_label)
        self.assertEqual(json_tree[3]["parentNodeId"], node_1_label + "_" + node_2_label + "_" + root_label)
        self.assertEqual(json_tree[3]["valueNode"], False)
        self.assertEqual(json_tree[3]["template"], "<div class=\"domStyle\"><span>shape</span></div>")
        self.assertEqual(json_tree[3]["label"], "shape")

        self.assertEqual(json_tree[4]["nodeId"], "density" + "_" + node_1_label + "_" + node_2_label + "_" + root_label)
        self.assertEqual(json_tree[4]["parentNodeId"], node_1_label + "_" + node_2_label + "_" + root_label)
        self.assertEqual(json_tree[4]["valueNode"], False)
        self.assertEqual(json_tree[4]["template"], "<div class=\"domStyle\"><span>density</span></div>")
        self.assertEqual(json_tree[4]["label"], "density")

        self.assertEqual(json_tree[5]["nodeId"], leaf_a_field + "_" + node_1_label + "_" + node_2_label + "_" +
                         root_label)
        self.assertEqual(json_tree[5]["parentNodeId"], node_1_label + "_" + node_2_label + "_" + root_label)
        self.assertEqual(json_tree[5]["valueNode"], False)
        self.assertEqual(json_tree[5]["template"], "<div class=\"domStyle\"><span>margin</span></div>")
        self.assertEqual(json_tree[5]["label"], leaf_a_field)

        self.assertEqual(json_tree[6]["nodeId"], leaf_a_label + "_" + leaf_a_field + "_" + node_1_label + "_" +
                         node_2_label + "_" + root_label)
        self.assertEqual(json_tree[6]["parentNodeId"], leaf_a_field + "_" + node_1_label + "_" + node_2_label + "_" +
                         root_label)
        self.assertEqual(json_tree[6]["valueNode"], True)
        self.assertEqual(json_tree[6]["lowConfidence"], True)
        self.assertEqual(json_tree[6]["template"], "<div class=\"domStyle\"><span>stervormige</span></div><span class="
                                                   "\"confidence\">55%</span>")
        self.assertEqual(json_tree[6]["label"], leaf_a_label)

        self.assertEqual(json_tree[7]["nodeId"], leaf_b_field + "_" + node_1_label + "_" + node_2_label + "_" +
                         root_label)
        self.assertEqual(json_tree[7]["parentNodeId"], node_1_label + "_" + node_2_label + "_" + root_label)
        self.assertEqual(json_tree[7]["valueNode"], False)
        self.assertEqual(json_tree[7]["template"], "<div class=\"domStyle\"><span>location</span></div>")
        self.assertEqual(json_tree[7]["label"], leaf_b_field)

        self.assertEqual(json_tree[8]["nodeId"], leaf_b_label + "_" + leaf_b_field + "_" + node_1_label + "_" +
                         node_2_label + "_" +
                         root_label)
        self.assertEqual(json_tree[8]["parentNodeId"], leaf_b_field + "_" + node_1_label + "_" + node_2_label + "_" +
                         root_label)
        self.assertEqual(json_tree[8]["valueNode"], True)
        self.assertEqual(json_tree[8]["template"], "<div class=\"domStyle\"><span>laterale bovenkwadrant linkermamma"
                                                   "</span></div><span class="
                                                   "\"confidence\">92%</span>")
        self.assertEqual(json_tree[8]["label"], leaf_b_label)

    def test_identifier_function(self):
        node_1_label = 'mass'
        node_2_label = 'positive_finding'
        node_3_label = 'negative_finding'
        root_label = 'root'

        report_node_1 = ReportNode(node_1_label, [], [])
        report_node_2 = ReportNode(node_2_label, [report_node_1], [])
        report_node_3 = ReportNode(node_1_label, [], [])
        report_node_4 = ReportNode(node_2_label, [report_node_3], [])
        report_node_5 = ReportNode(node_1_label, [], [])
        report_node_6 = ReportNode(node_3_label, [report_node_5], [])
        report_node_7 = ReportNode(node_1_label, [], [])
        report_node_8 = ReportNode(node_3_label, [report_node_7], [])
        root = ReportNode(root_label, [report_node_2, report_node_4, report_node_6, report_node_8], [])
        json_tree = view.generate_tree(root)

        self.assertEqual(json_tree[0]["nodeId"], root_label)
        self.assertEqual(json_tree[0]["parentNodeId"], None)
        self.assertEqual(json_tree[0]["valueNode"], False)
        self.assertEqual(json_tree[0]["template"], "<div class=\"domStyle\"><span>root</span></div>")
        self.assertEqual(json_tree[0]["label"], root_label)

        self.assertEqual(json_tree[1]["nodeId"], node_2_label + "_" + root_label)
        self.assertEqual(json_tree[1]["parentNodeId"], root_label)
        self.assertEqual(json_tree[1]["valueNode"], False)
        self.assertEqual(json_tree[1]["template"], "<div class=\"domStyle\"><span>positive_finding</span></div>")
        self.assertEqual(json_tree[1]["label"], node_2_label)

        self.assertEqual(json_tree[2]["nodeId"], node_1_label + "_" + node_2_label + "_" + root_label)
        self.assertEqual(json_tree[2]["parentNodeId"], node_2_label + "_" + root_label)
        self.assertEqual(json_tree[2]["valueNode"], False)
        self.assertEqual(json_tree[2]["template"], "<div class=\"domStyle\"><span>mass</span></div>")
        self.assertEqual(json_tree[2]["label"], node_1_label)

        self.assertEqual(json_tree[3]["nodeId"], node_2_label + "_" + root_label + "2")
        self.assertEqual(json_tree[3]["parentNodeId"], root_label)
        self.assertEqual(json_tree[3]["valueNode"], False)
        self.assertEqual(json_tree[3]["template"], "<div class=\"domStyle\"><span>positive_finding</span></div>")
        self.assertEqual(json_tree[3]["label"], node_2_label)

        self.assertEqual(json_tree[4]["nodeId"], node_1_label + "_" + node_2_label + "_" + root_label + "2")
        self.assertEqual(json_tree[4]["parentNodeId"], node_2_label + "_" + root_label + "2")
        self.assertEqual(json_tree[4]["valueNode"], False)
        self.assertEqual(json_tree[4]["template"], "<div class=\"domStyle\"><span>mass</span></div>")
        self.assertEqual(json_tree[4]["label"], node_1_label)

        self.assertEqual(json_tree[5]["nodeId"], node_3_label + "_" + root_label)
        self.assertEqual(json_tree[5]["parentNodeId"], root_label)
        self.assertEqual(json_tree[5]["valueNode"], False)
        self.assertEqual(json_tree[5]["template"], "<div class=\"domStyle\"><span>negative_finding</span></div>")
        self.assertEqual(json_tree[5]["label"], node_3_label)

        self.assertEqual(json_tree[6]["nodeId"], node_1_label + "_" + node_3_label + "_" + root_label)
        self.assertEqual(json_tree[6]["parentNodeId"], node_3_label + "_" + root_label)
        self.assertEqual(json_tree[6]["valueNode"], False)
        self.assertEqual(json_tree[6]["template"], "<div class=\"domStyle\"><span>mass</span></div>")
        self.assertEqual(json_tree[6]["label"], node_1_label)

        self.assertEqual(json_tree[7]["nodeId"], node_3_label + "_" + root_label + "2")
        self.assertEqual(json_tree[7]["parentNodeId"], root_label)
        self.assertEqual(json_tree[7]["valueNode"], False)
        self.assertEqual(json_tree[7]["template"], "<div class=\"domStyle\"><span>negative_finding</span></div>")
        self.assertEqual(json_tree[7]["label"], "negative_finding")

        self.assertEqual(json_tree[8]["nodeId"], node_1_label + "_" + node_3_label + "_" + root_label + "2")
        self.assertEqual(json_tree[8]["parentNodeId"], node_3_label + "_" + root_label + "2")
        self.assertEqual(json_tree[8]["valueNode"], False)
        self.assertEqual(json_tree[8]["template"], "<div class=\"domStyle\"><span>mass</span></div>")
        self.assertEqual(json_tree[8]["label"], node_1_label)

    def test_apply_changes(self):
        leaf_a_label = 'stervormige'
        leaf_a_field = 'margin'

        report_leaf_a = ReportLeaf(leaf_a_label, leaf_a_field, 0.55,
                                   {'stervormige': 55, 'circumscribed': 0, 'obscured': 0})
        report_node_1 = ReportNode('mass', [report_leaf_a], ['shape', 'margin', 'density'])
        report_node_2 = ReportNode('positive_finding', [report_node_1], [])
        root = ReportNode('root', [report_node_2], [])
        json_tree = view.generate_tree(root)

        self.assertEqual(json_tree[6]["nodeId"], leaf_a_label + "_" + leaf_a_field + "_mass_positive_finding_root")
        self.assertEqual(json_tree[6]["parentNodeId"], leaf_a_field + "_mass_positive_finding_root")
        self.assertEqual(json_tree[6]["valueNode"], True)
        self.assertEqual(json_tree[6]["template"], '<div class="domStyle"><span>stervormige</span>'
                                                   '</div><span class="confidence">55%</span>')
        self.assertEqual(json_tree[6]["label"], leaf_a_label)

        leaf_a_id = json_tree[6]["nodeId"]
        leaf_a_new_label = "circumscribed"
        json_tree = view.generate_tree(root, {leaf_a_id: leaf_a_new_label})

        self.assertEqual(json_tree[6]["nodeId"], leaf_a_label + "_" + leaf_a_field + "_mass_positive_finding_root")
        self.assertEqual(json_tree[6]["parentNodeId"], leaf_a_field + "_mass_positive_finding_root")
        self.assertEqual(json_tree[6]["valueNode"], True)
        self.assertEqual(json_tree[6]["template"], '<div class="domStyle"><span>circumscribed</div></span>'
                                                   '<span class="material-icons">mode</span>')
        self.assertEqual(json_tree[6]["label"], leaf_a_new_label)
