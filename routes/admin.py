from flask import Blueprint, jsonify, request
from util.auth.authenticator import requires_admin
from handlers.database_handler import DatabaseHandler
from handlers.message_creator import MessageCreator
from util.debug import print_request
import uuid
import config
from MQTT.mqtt_client import open_admin_link, close_admin_link, send_message_admin

admin_route = Blueprint('admin_route', __name__, url_prefix="/admin")


@admin_route.route('/get_routers', methods=['POST'])
@requires_admin
def get_routers():
    return jsonify(DatabaseHandler().get_routers()), 200


@admin_route.route("/get_sensors", methods=['POST'])
@requires_admin
def get_sensors():
    return jsonify(DatabaseHandler().get_sensors()), 200


@admin_route.route("/get_home_data", methods=['POST'])
@requires_admin
@print_request
def get_home_data():
    routers = DatabaseHandler().get_routers()
    routers_total = len(routers)
    routers_online = 0
    for router in routers[:]:
        status = DatabaseHandler().get_router_status(router['router_id'])
        if status is True:
            routers_online = routers_online + 1
    routers_claimed = 0
    for router in routers[:]:
        id = router['router_id']
        owner = DatabaseHandler().get_router_owner(id)
        if owner is None:
            routers_claimed = routers_claimed + 1
    routers_unclaimed = routers_total - routers_claimed
    sensors = DatabaseHandler().get_sensors()
    sensors_total = len(sensors)
    sensors_claimed = 0
    for sensor in sensors[:]:
        result = DatabaseHandler().is_sensor_claimed(sensor['sensor_id'])
        if result is True:
            sensors_claimed = sensors_claimed + 1
    sensor_online = 0
    for sensor in sensors[:]:
        owner = sensor['router']
        if owner is not None:
            res = DatabaseHandler().get_router_status(owner)
            if res is True:
                sensor_online = sensor_online + 1
    sensor_unclaimed = sensors_total - sensors_claimed
    users_total = len(DatabaseHandler().get_users())
    return jsonify(routers={"total": routers_total, "online": routers_online, "claimed": routers_unclaimed, "unclaimed": routers_claimed},
                sensors={"total": sensors_total, "claimed": sensors_claimed, "unclaimed": sensor_unclaimed, "online": sensor_online},
                users={"total": users_total}), 200


@admin_route.route("/create_data_link", methods=['POST'])
@requires_admin
@print_request
def setup_link():
    topic_name = str(uuid.uuid4())
    open_admin_link(topic_name)
    return jsonify(topic_name=topic_name), 200


@admin_route.route("/close_data_link", methods=['POST'])
@requires_admin
def close_link():
    topic_name = request.json['topic_name']
    close_admin_link(topic_name)


@admin_route.route("/add_router", methods=['POST'])
@requires_admin
def add_router():
    return jsonify(result=DatabaseHandler().add_router(request.json['router_id'])), 200


# TODO remove router references
@admin_route.route("/remove_router", methods=['POST'])
@print_request
@requires_admin
def remove_router():
    DatabaseHandler().remove_router(request.json['router_id'])
    return jsonify(result=True), 200


@admin_route.route("/test", methods=['POST'])
@requires_admin
@print_request
def test():
    message = MessageCreator(MessageCreator.PING, "dd")
    send_message_admin(message)
    return jsonify(True), 200
