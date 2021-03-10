"""
Imports
"""

import json
import jsonpickle

from flask import request, Response
from flask_restful import Resource, reqparse, abort

from src.model.mammo.wrapper import Wrapper

parser = reqparse.RequestParser()
mammo_nlp = Wrapper()
parser.add_argument('text', type=str, required=True, help="Include the plaintext that needs checking by the Mammo NLP")


class Mammo(Resource):
    """
       HTTPResource for mammography, connects to the Mammography NLP and creates HTTPResponse
    """

    def get(self, args):
        """
        Process the given text for mammography
        :return: Returns HTTPResponse containing JSON object with status code and probability list
        """
        if not args['text']:
            abort(404, message="Text needed for nlp processing")
        text = args["text"]
        problist = mammo_nlp.process(text)
        frozen = jsonpickle.encode(problist)
        return {"Response": 200, "Data": frozen}
