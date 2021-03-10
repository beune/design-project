"""
Imports
"""
import pickle

from src.report_node import ReportNode


def get_parsed_text(environment: str, text: str) -> ReportNode:
    """
    Send the text to the server to retrieve a ReportTree.
    :param environment: The environment that should interpret the text.
    :param text: The text to be interpreted.
    :return: A ReportNode containing the desired structure.
    """
    # TODO: This is a temporary
    with open('TESTPICKLE.pkl', 'rb') as file:
        return pickle.load(file)


if __name__ == "__main__":
    tree = get_parsed_text('', '')
    print("end")
