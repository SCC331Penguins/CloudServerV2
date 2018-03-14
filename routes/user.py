from flask import jsonify, request, Blueprint
from handlers.database_handler import DatabaseHandler
from util.auth import authenticator
from util.debug import print_request
from MQTT.mqtt_client import send_message_admin, send_user_update

user = Blueprint('user', __name__, url_prefix='/user')


# Allows user to login
@user.route("/login", methods=['POST'])
@print_request
def login():
    username = request.json['username']
    password = request.json['password']
    resp = DatabaseHandler().login_user(username, password)
    if resp[0][0] is True:
        send_message_admin("USER LOGIN", "By user " + str(username) + ", logged in")
    else:
        send_message_admin("USER LOGIN", "By user " + str(username) + ", does not exist")
    return jsonify(logged_in=resp[0][0], token=resp[0][1]), 200


# Register user on server
@user.route("/register", methods=['POST'])
@print_request
def register():
    username = request.json['username']
    password = request.json['password']
    resp = DatabaseHandler().register_user(username, password)
    if resp is not False:
        send_message_admin("USER REGISTER", "New user " + str(username))
        print(resp)
        send_user_update(resp['username'], remove=False, id=resp['id'])
        resp = True
    return jsonify(resp), 200


# Allows a user to claim a router
@user.route("/claim_router", methods=['POST'])
@authenticator.requires_token
@print_request
def claim_router():
    router_id = request.json['router_id']
    resp = DatabaseHandler().claim_router(router_id, request.json['token'])
    if resp is True:
        send_message_admin(
            "USER CLAIM", "By user " + DatabaseHandler().get_user_from_id(request.json['token']) + " to router " + str(request.json['router_id']))
    return jsonify(result=resp), 200


@user.route("/auth_user_add", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request
def authenticate_user():
    router_id = request.json['router_id']
    username = request.json['username']
    result = DatabaseHandler().get_user(username=username)
    if result is None:
        return jsonify(result=False), 201
    id = result.id
    result = DatabaseHandler().add_auth_user(id, router_id)
    if result is False:
        return jsonify(False), 201
    return jsonify(id=id, username=username), 200


@user.route("/auth_user_remove", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
@print_request
def remove_authenticated_user():
    router_id = request.json['router_id']
    username = request.json['username']
    result = DatabaseHandler().get_user(username=username)
    if result is None:
        return jsonify(result=False), 201
    id = result.id
    result = DatabaseHandler().remove_auth_user(id, router_id)
    if result is False:
        return jsonify(False), 201
    return jsonify(id=id, username=username), 200


@user.route("/get_auth_users", methods=['POST'])
@authenticator.requires_token
@authenticator.requires_ownership
def get_authed():
    router_id = request.json['router_id']
    result = DatabaseHandler().get_authed_users(router_id)
    if result is None:
        return jsonify(result=[]), 201
    return jsonify(result), 200
