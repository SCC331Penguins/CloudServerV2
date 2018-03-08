from flask import Flask, jsonify, request, Blueprint
from util.auth import authenticator
from util.debug import print_request
from MQTT.mqtt_client import client

debug = Blueprint('debug', __name__, url_prefix='/debug')


@debug.route("/", methods=['GET'])
@print_request
def test():
    client.publish("test", "test")
    return jsonify(True), 200


@debug.route("/router", methods=['GET'])
@print_request
def get_token():
    return jsonify(authenticator.generate_token("SCC33102_R01")), 200


@debug.route("/token", methods=['POST'])
@authenticator.requires_token
@print_request
def check_token():
    return jsonify(True), 200
