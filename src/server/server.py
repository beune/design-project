"""
Imports
"""
import jsonpickle
from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from environments.environment import envs

app = Flask(__name__)
api = Api(app)


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
    return envs[environment].get(data)


app.run()