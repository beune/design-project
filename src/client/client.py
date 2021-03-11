"""
Imports
"""
import requests
import jsonpickle


def connect():
    """
    Method used to test API calls
    """
    text = "X-mammografie beiderzijds: Een stervormige laesie laterale bovenkwadrant linkermamma"
    data = {"text": text}
    # r = requests.get("http://127.0.0.1:5000/mammo/", params=data)
    r = requests.get("http://127.0.0.1:5000/mammo/", json=data)
    rootnode = jsonpickle.decode(r.json()["Data"])
    print("OUTPUT FROM MAMMO:", rootnode)
    # hersendata = {"text": "foo"}
    # r = requests.get("http://127.0.0.1:5000/hersen/", json=hersendata)
    # hersenlist = r.json()["Data"]
    # print("OUTPUT FROM HERSEN:", hersenlist)


if __name__ == '__main__':
    connect()
