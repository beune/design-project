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
    def __init__(self):
        report_leaf = ReportLeaf("stervormige", "margin", 0.55, )
        self.input = None

    def test_build_json_tree(self):
        json_tree = view.generate_tree(self.input)
    #     self.assertEqual(json_tree)
    #
    # def test_hash_function(self):
    #
    #
    # def test_apply_changes(self):


