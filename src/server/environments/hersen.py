"""
Imports
"""
from src.model.report_node import ReportNode

expected = {}
hints = {}


def parse(text: str) -> ReportNode:
    """
    Method used to process hersen text
    :param text: Text that needs processing
    :return: For now a stub reportnode, as hinternlp is not implemented
    """
    return ReportNode("STUB, YOU ENTERED: " + text, [], [])
