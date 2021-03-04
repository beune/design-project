"""
Imports
"""
import xml.etree.ElementTree as ET
from report_node import ReportNode
from report_leaf import ReportLeaf


class Itemizer:
    """
    Class used to create the item representation of a XML return
    """

    def parse(self, input_file) -> ReportNode:
        """
        :param input_file:
        :return:
        """
        with open(input_file, 'r') as f:
            root = ET.parse(f).getroot()
        return self.parse_node(root)

    def get_prob(self, text):
        """

        :param text:
        :return:
        """
        return 0

    def parse_node(self, node: ET.Element):
        """

        :param node:
        """
        if not node:
            item = ReportLeaf(" ".join(node.text.split()), node.tag, self.get_prob(node.text))
        else:
            item = ReportNode(node.tag)
            for child in node:
                newitem = self.parse_node(child)
                item.add_child(newitem)
        return item

    def create(self, prob_list, parent):
        """
        Method used to create an item representation
        :param parent: The parent node for which the prob_list are children
        :param prob_list: The list of items with probabilities
        """
        j = 0
        label = prob_list[j][1]
        for i in range(len(prob_list)):
            if prob_list[i][1] != label:
                parent.add_child(prob_list[j:i])
                j = i
        return parent

    def getavgprob(self, prob_list):
        """
        Method used to retrieve the average certainty of parts of a prob_list
        :param prob_list: The list of items
        :return: The average certainty
        """
        total = 0
        for i in range(len(prob_list)):
            total += prob_list[i][2]
        avg = total / len(prob_list)
        return avg


if __name__ == "__main__":
    i = Itemizer()
    res = i.parse("tester.xml")
    print("lol")
    print("succes")
