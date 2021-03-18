"""
Imports
"""

import unittest
from multiprocessing import Process

import jsonpickle
import requests

from report_tree.report_node import ReportNode
from server import server


class HTTPTest(unittest.TestCase):

    def test_get(self):
        text = "THIS IS A TEST CASE"
        data = {"text": text}
        pr = Process(target=server.run)
        pr.start()
        response = requests.get("http://127.0.0.1:8000/hersen/", json=data)
        self.assertEqual(ReportNode, type(jsonpickle.decode(response.json()["Data"])))
        self.assertEqual(200, response.status_code)
        pr.terminate()
        pr.join()
