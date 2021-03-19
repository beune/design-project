"""
Imports
"""
from report_tree.report_node import ReportNode
from report_tree.report_leaf import ReportLeaf

expected = {}
hints = {}


def parse(text: str) -> ReportNode:
    """
    Method used to process hersen text
    :param text: Text that needs processing
    :return: For now a stub reportnode, as hinternlp is not implemented
    """

    root = ReportNode("root", [], [])
    pos1 = ReportNode("positive finding", [], [])
    mass1 = ReportNode("mass", [], ["size", "location"])
    size1 = ReportLeaf("ongeveer 2, 3 cm", "size", 0.75, hint="The size of the mass")
    multifocality1 = ReportNode("Multifocality", [], [])
    hin = ("Multiple tumors in the brain usually indicate metastatic disease (figure)."
           "Primary brain tumors are typically seen in a single region, but some brain tumors like lymphomas, "
           "multicentric glioblastomas and gliomatosis cerebri can be multifocal. Some tumors can be multifocal"
           " as a result of seeding metastases: this can occur in medulloblastomas (PNET-MB), ependymomas, GBMs "
           "and oligodendrogliomas. Meningiomas and schwannomas can be multiple, especially in neurofibromatosis"
           " type II")
    mass1.add_child(multifocality1)
    mass1.add_child(size1)
    neur = ReportLeaf("Neurofibromatose twee", "Neurofibromatosis II", 0.80,
                      {"meningiomas": 0.79, "ependymomas": 0.47, "choroid plexus papillomas": 0.11}, hin)
    pos1.add_child(pos1.add_child(mass1.add_child(multifocality1.add_child(neur))))

    root.add_child(pos1)

    return root
