"""
Imports
"""
from report_tree.report_node import ReportNode
from report_tree.report_leaf import TextLeaf, LabelLeaf

expected = {}
hints = {}

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


def parse(text: str) -> ReportNode:
    """
    Method used to process hersen text
    :param text: Text that needs processing
    :return: For now a stub reportnode, as hinternlp is not implemented
    """

    root = ReportNode("root", [], [])
    pos1 = ReportNode("positive finding", [], [])
    mass1 = ReportNode("mass", [], ["size", "location"])
    size1 = TextLeaf("size", 0.75, "ongeveer 2, 3 cm", hint="The size of the mass")
    multifocality1 = ReportNode("Multifocality", [], [])
    hin = ("Multiple tumors in the brain usually indicate metastatic disease (figure)."
           "Primary brain tumors are typically seen in a single region, but some brain tumors like lymphomas, "
           "multicentric glioblastomas and gliomatosis cerebri can be multifocal. Some tumors can be multifocal"
           " as a result of seeding metastases: this can occur in medulloblastomas (PNET-MB), ependymomas, GBMs "
           "and oligodendrogliomas. Meningiomas and schwannomas can be multiple, especially in neurofibromatosis"
           " type II")
    types = {"meningiomas", "ependymomas", "choroid plexus papillomas"}
    mass1.add_child(size1)
    neur = LabelLeaf("Neurofibromatosis II", 0.80, "zichtbaar ependymomas", types, ("ependymomas", .8), hint=hin)
    multifocality1.add_child(neur)
    mass1.add_child(multifocality1)
    pos1.add_child(mass1)
    root.add_child(pos1)

    return root
