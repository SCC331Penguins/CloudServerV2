from flask import jsonify, request, Blueprint
from handlers.database_handler import DatabaseHandler
from MQTT.database_handler import DatabaseHandler as HistoricHandler
from util.auth import authenticator
from util.debug import print_request

historic = Blueprint('historic', __name__, url_prefix='/historic')


@historic.route("/get_history", methods=['POST'])
@print_request
def get_history():
    # id = authenticator.verify_token(request.json['token'])
    router_id = request.json['router_id']
    sensor_id = request.json['sensor_id']
    start = request.json['start']
    end = request.json['end']
    print(request.json)

    if start == 0 or end == 0:
        start = None
        end = None

    hh = HistoricHandler()

    if sensor_id == "ALL":
        data = {}
        db = DatabaseHandler()
        sensors = db.get_router_sensors(router_id)

        for x in sensors[:]:
            s_id = x[0]
            res = hh.get_reading(router_id, s_id, start=start, end=end)
            print("Results: " + res)
            data.update({s_id: res})

        return jsonify(data=data)

    result = hh.get_reading(router_id, sensor_id, start=start, end=end)
    ret = {}
    ret.update({sensor_id: result})

    return jsonify(data=ret)
