from flask import jsonify, request, Blueprint
from handlers.database_handler import DatabaseHandler
from util.auth import authenticator
from util.debug import print_request

user = Blueprint('user', __name__, url_prefix='/user')


# Allows user to login
@user.route("/login", methods=['POST'])
@print_request
def login():
    username = request.json['username']
    password = request.json['password']
    resp = DatabaseHandler().login_user(username, password)
    return jsonify(logged_in=resp[0][0], token=resp[0][1]), 200


# Register user on server
@user.route("/register", methods=['POST'])
@print_request
def register():
    username = request.json['username']
    password = request.json['password']
    resp = DatabaseHandler().register_user(username, password)
    return jsonify(resp), 200


# Allows a user to claim a router
@user.route("/claim_router", methods=['POST'])
@authenticator.requires_token
@print_request
def claim_router():
    router_id = request.json['router_id']
    resp = DatabaseHandler().claim_router(router_id, request.json['token'])
    return jsonify(result=resp), 200
