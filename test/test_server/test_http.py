"""
Imports
"""

import unittest
from multiprocessing import Process

import jsonpickle
import requests

from reporttree.node import Node
from server_package import server


class HTTPTest(unittest.TestCase):

    def test_get(self):
        text = "THIS IS A TEST CASE"
        data = {"text": text}
        pr = Process(target=server.run)
        pr.start()
        response = requests.get("http://127.0.0.1:5000/env/hersen/", json=data)
        node = jsonpickle.decode(response.json()["Data"])
        self.assertIsInstance(node, Node)
        self.assertEqual(200, response.status_code)
        pr.terminate()
        pr.join()
