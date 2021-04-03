"""
Imports
"""
from reporttree.node import Node
from reporttree.label_node import LabelNode

EXPECTED = {}
OPTIONS = {}
HINTS = {}

COLOURS = {"size": "#E71212",
           "Neurofibromatosis II": "#E77C12",
           "margin": "#EDED12",
           "location": "#13EBEB",
           "morphology": "#1313EB",
           "associated_features": "#D981D9",
           "distribution": "#81ADD9",
           }


def get_colours() -> dict:
    """
    Method used to retrieve the colour palette of the mammo environment
    :return: Dictionary with labels mapped to colours
    """
    return COLOURS


def parse(text: str) -> Node:
    """
    Method used to process hersen text
    :param text: Text that needs processing
    :return: For now a stub reportnode, as hinternlp is not implemented
    """

    text = "ongeveer 2, 3 cm zichtbaar ependymomas"
    root = Node("report", (text, 96))
    pos1 = Node("positive finding", (text, 96))
    mass1 = Node("mass", (text, 96))
    size1 = Node("size", ("ongeveer 2, 3 cm", 40), hint="The size of the mass")
    multifocality1 = Node("Multifocality", ("zichtbaar ependymomas", 80))
    hin = ("Multiple tumors in the brain usually indicate metastatic disease (figure)."
           "Primary brain tumors are typically seen in a single region, but some brain tumors like lymphomas, "
           "multicentric glioblastomas and gliomatosis cerebri can be multifocal. Some tumors can be multifocal"
           " as a result of seeding metastases: this can occur in medulloblastomas (PNET-MB), ependymomas, GBMs "
           "and oligodendrogliomas. Meningiomas and schwannomas can be multiple, especially in neurofibromatosis"
           " type II")
    types = ["meningiomas", "ependymomas", "choroid plexus papillomas"]
    mass1.add_child(size1)
    neur = LabelNode("Neurofibromatosis II", types, ("zichtbaar ependymomas", 80), ("ependymomas", 80), hint=hin)
    multifocality1.add_child(neur)
    mass1.add_child(multifocality1)

    # speculative child
    location = Node("location")
    mass1.add_child(location)

    pos1.add_child(mass1)
    root.add_child(pos1)

    return root
