from flask import jsonify, request, Blueprint
from handlers.database_handler import DatabaseHandler
from handlers.message_creator import MessageCreator
from util.auth import authenticator
from util.debug import print_request, print_request_short
from MQTT.mqtt_client import send_message, send_message_admin
import uuid

api = Blueprint('api', __name__, url_prefix='/api')


# Open a Live Data Channel
@api.route("/requestLiveData", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request
def request_live_data():
    router_id = request.json['router_id']
    if DatabaseHandler().user_has_router(router_id, request.json['token']) is False:
        return jsonify(result=False)
    topic_name = str(uuid.uuid4())
    message = MessageCreator(MessageCreator.NEW_CHANNEL, topic_name)
    send_message(router_id, message)
    send_message_admin("API", "New Live data link by user " + DatabaseHandler().get_user_from_id(request.json['token']) + " to router " + str(router_id))
    return jsonify(topic_name=topic_name), 200


# Send phone location
@api.route("/phone_location", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request
def phone_location():
    router_id = request.json['router_id']
    message = MessageCreator(MessageCreator.PHONE_LOCATION, request.json['sensor_id'])
    send_message(router_id, message)
    return jsonify(True), 200


@api.route("/arm_system", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request
def arm_system():
    router_id = request.json['router_id']
    arm = request.json['armed']
    message = MessageCreator(MessageCreator.ARM_SYSTEM, arm)
    send_message(router_id, message)
    return jsonify(True), 200


# Control actuators
@api.route("/actuator_control", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request
def control_actuator():
    router_id = request.json['router_id']
    message = MessageCreator(MessageCreator.COMMAND, {'MAC': request.json['MAC'], "command": request.json['command']})
    send_message(router_id, message)
    send_message_admin("API", "Actuator control by user " + DatabaseHandler().get_user_from_id(request.json['token']) + " to router " + str(router_id))
    return jsonify(True), 200


# Set buttons
@api.route("/set_button", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request_short
def set_internet_button():
    router_id = request.json['router_id']
    message = MessageCreator(MessageCreator.CONFIG_BUTTON, request.json['buttons'])
    send_message(router_id, message)
    return jsonify(True), 200
