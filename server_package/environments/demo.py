"""
This environment serves as a simplified demo
"""
from reporttree.node import Node
from reporttree.label_node import LabelNode

EXPECTED = {}
OPTIONS = {}

COLOURS = {
    "breast composition": "#E71212",
    "shape": "#E77C12",
    "margin": "#EDED12",
    "size": "#13EB13",
    "location": "#13EBEB",
    "morphology": "#1313EB",
    "associated_features": "#D981D9",
    "distribution": "#81ADD9",
    "architectural_distortion": "#A9C9CF",
}


HINTS = {
    "breast composition": "In the BI-RADS edition 2013 the assignment of the breast composition is changed into a, b, c"
                          "and d-categories followed by a description: \n"
                          "- A The breast are almost entirely fatty. Mammography is highly sensitive in this setting.\n"
                          "- B There are scattered areas of fibroglandular density. The term density describes the degr"
                          "ee of x-ray attenuation of breast tissue but not discrete mammographic findings.\n"
                          "- C The breasts are heterogeneously dense, which may obscure small masses."
                          "Some areas in the breasts are sufficiently dense to obscure small masses.\n"
                          "- D The breasts are extremely dense, which lowers the sensitivity of mammography"
}


def parse(text: str) -> Node:
    """
    Method used to process hersen text
    :param text: Text that needs processing
    :return: For now a stub reportnode, as hinternlp is not implemented
    """

    text = "Star-shaped lesion in left breast lesion has a size of 2 cm Breasts are entirely fatty"
    shape = LabelNode("shape", ["oval", "round", "irregular"], ("Star-shaped", 92), ("irregular", 72))
    other = Node("O", ("lesion in left breast lesion has a size of", 89))
    size = Node("size", ("2 cm", 87))
    density = LabelNode("density", ["fat", "low", "equal", "high"])
    mass = Node("mass", ("Star-shaped lesion in left breast lesion has a size of 2 cm", 95), [shape, other, size, density])

    other = Node("O", ("Breasts are", 51))
    comp = LabelNode("breast composition", ["A", "B", "C", "D"], ("entirely fatty", 93), ("A", 99))

    root = Node("report", (text, 0), [mass, other, comp])
    return root
