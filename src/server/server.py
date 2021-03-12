"""
Imports
"""
import jsonpickle
from flask import Flask, request
from flask_restful import Api, abort
from src.server.environment import envs

app = Flask(__name__)
api = Api(app)


def run():
    """
    Method used to run the server
    """
    app.run()


@app.route("/")
def home():
    """
    Stub method to test the REST API
    :return:
    """
    return "HELLO WORLD"


@app.route("/<string:environment>/", methods=['GET'])
def get(environment):
    """
    Method used to get the right environment
    :param environment: The current selected environment, functions as endpoint
    :return: Returns the HTTPResponse generated by the selected environment
    """
    data = request.get_json()

    # envs[environment].get(data)
    if not data['text']:
        abort(404, message="Text needed for nlp processing")
    text = data["text"]
    ret = jsonpickle.encode(envs[environment].process(text))
    return {"Response": 200, "Data": ret}


if __name__ == "__main__":
    run()