"""
Imports
"""
from flask_restful import Resource, reqparse, abort
parser = reqparse.RequestParser()
parser.add_argument('text', type=str, required=True, help="Include the plaintext that needs checking by the Mammo NLP")


class Hersen:
    """
    Class used for Hersen environment
    """
    def get(self, args):
        """
        Process the given text for mammography
        :return: Returns the HTTPResponse with the
        """
        if not args['text']:
            abort(404, message="Text needed for nlp processing")
        text = args["text"]
        problist = ["Dit is hersen environment"]
        return {"Response": 200, "Data": problist}
