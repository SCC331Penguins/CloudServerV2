from flask import jsonify, request, Blueprint
from handlers.database_handler import DatabaseHandler
from util.auth import authenticator
from util.debug import print_request
from handlers.message_creator import MessageCreator
from MQTT.mqtt_client import send_message

sensor_route = Blueprint('sensor_route', __name__, url_prefix='/sensor')


# get sensors of a router
@sensor_route.route('/get_sensors', methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request
def get_sensors():
    result = DatabaseHandler().get_router_sensors(request.json['router_id'])
    return jsonify(result), 200


# set config for sensors
@sensor_route.route("/set_config", methods=['POST'])
@authenticator.requires_token
@print_request
def set_config():
    sensors = request.json["sensors"]
    payload = []
    for sensor in sensors[:]:
        DatabaseHandler().set_sensor_config(sensor['id'], sensor['config'])
        payload.append({"id": sensor['id'], "config": sensor['config']})
    message = MessageCreator(MessageCreator.UPDATE_SENSORS, payload)
    send_message(request.json['router_id'], message)
    return jsonify(True), 200
