"""
Imports
"""
import jsonpickle
from flask import Flask, request
from flask_restful import Api, abort

from servpackage import environment

app = Flask(__name__)
api = Api(app)


def run():
    """
    Method used to run the server
    """
    app.run(port=5000, host="127.0.0.1")


@app.route("/")
def home():
    """
    Home endpoint
    :return: Returns HTTPResponse with available environments as data
    """
    envs = {environment.ENVS[endpoint].name: endpoint for endpoint in environment.ENVS}
    return {"Response": 200, "Data": envs}


@app.route("/env/<env_selected>/", methods=['GET'])
def get(env_selected):
    """
    Method used to get the right environment
    :param env_selected: The current selected environment, functions as endpoint
    :return: Returns the HTTPResponse generated by the selected environment
    """
    data = request.get_json()

    # envs[environment].get(data)
    if not data['text']:
        abort(404, message="Text needed for nlp processing")
    text = data["text"]
    ret = jsonpickle.encode(environment.ENVS[env_selected].process(text))
    return {"Response": 200, "Data": ret}


if __name__ == "__main__":
    run()
