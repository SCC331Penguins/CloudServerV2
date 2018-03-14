from flask import jsonify, request, Blueprint
from handlers.database_handler import DatabaseHandler
from handlers.message_creator import MessageCreator
from util.auth import authenticator
from util.debug import print_request, print_request_short
from MQTT.mqtt_client import send_message, send_message_admin
import uuid

api = Blueprint('devPanel', __name__, url_prefix='/devPanel')


# Open a Live Data Channel
@api.route("/Routers", methods=['POST'])
@authenticator.requires_dev_admin
def Routers():
    
    return jsonify(topic_name=topic_name), 200
