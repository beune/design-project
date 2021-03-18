"""
Imports
"""
import requests
import jsonpickle


def connect():
    """
    Method used to test API calls
    """
    # text = "X-mammografie beiderzijds: Een stervormige laesie laterale bovenkwadrant linkermamma, De laesie heeft een body van ongeveer 2,3 cm, De laesie is wel moeilijk af te grenzen van het normale klierweefsel,  In en rondom de laesie geen microcalcificaties, In de rechtermamma voor zover te beoordelen geen aanwijzingen voor maligniteit, Axillair beiderzijds geen pathologische lymfeklieren zichtbaar, "
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
