from flask import jsonify, request, Blueprint
from handlers.database_handler import DatabaseHandler
from util.auth import authenticator
from util.debug import print_request, print_request_short
from MQTT.mqtt_client import send_message, send_message_admin
from handlers.message_creator import MessageCreator


router_route = Blueprint('router_route', __name__, url_prefix='/router')


# Get routers for users
@router_route.route('/get_router', methods=['POST'])
@authenticator.requires_token
@print_request
def get_routers():
    res = DatabaseHandler().get_user_routers(request.json['token'])
    send_message_admin("GET ROUTER", "Get router request from user " + DatabaseHandler().get_user_from_id(request.json['token']))
    return jsonify(res), 200


# Set a script for a router
@router_route.route("/set_script", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request_short
def set_script():
    router_id = request.json['router_id']
    script = request.json['script']
    res = DatabaseHandler().add_script(router_id, script)
    if res is True:
        scripts = DatabaseHandler().get_script(router_id=router_id)
        scripts_list = []
        for x in scripts[:]:
            scripts_list.append(x.script)
        message = MessageCreator(MessageCreator.UPDATE_SCRIPT, scripts_list)
        send_message(router_id, message)
    send_message_admin("POST SCRIPT", "Nw script added by user " + DatabaseHandler().get_user_from_id(request.json['token']) + " to router " + str(router_id))
    return jsonify(res), 200


# Get script for a router
@router_route.route("/get_script", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request
def get_script():
    # TODO get script
    return jsonify(True), 200


@router_route.route("/get_actuators", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request
def get_actuators():
    res = DatabaseHandler().get_actuators(request.json['router_id'])
    send_message_admin(
        "GET ACTUATOR", "by user " + DatabaseHandler().get_user_from_id(request.json['token']) + " from router " + str(request.json['router_id']))
    return jsonify(res), 200
