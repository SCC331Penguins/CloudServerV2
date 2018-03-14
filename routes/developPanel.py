import time
from flask import jsonify, request, Blueprint
from handlers.database_handler import DatabaseHandler
from handlers.message_creator import MessageCreator
from util.auth import authenticator
from util.debug import print_request, print_request_short
from MQTT.mqtt_client import send_message, send_message_admin
import json

developPanel = Blueprint('devPanel', __name__, url_prefix='/devPanel')


# getAllRouters and there warnings
@developPanel.route("/Routers", methods=['GET'])
@authenticator.requires_dev_admin
def Routers():
    db = DatabaseHandler()

    routers = db.getAllRouters()
    newRouters = []
    router_warnings = db.getAllRouterWarnings()
    for router in routers:
        newRouter = {}
        newRouter['name'] = router.router_id
        newRouter['lastOnline'] = router.last_heard
        newRouter['warnings'] = []
        for warning in router_warnings:
            if warning.originName == router.router_id:
                new_warning = {}
                new_warning['level'] = warning.w_level
                new_warning['msg'] = warning.w_msg
                new_warning['time'] = warning.w_time
                newRouter['warnings'].append(new_warning)
        newRouters.append(newRouter)
    return jsonify(newRouters), 200

@developPanel.route("/Router/<id>/", methods=['GET'])
@authenticator.requires_dev_admin
def Router(id=None):
    if(id == None):
        return jsonify(None), 400
    db = DatabaseHandler()
    router= db.getRouter(id)
    router_warnings = db.getRouterWarnings(id)
    newRouter = {}
    newRouter['name'] = router.router_id
    newRouter['lastOnline'] = router.last_heard
    newRouter['actuators'] = db.get_actuators(id)
    newRouter['warnings'] = []
    for warning in router_warnings:
            new_warning = {}
            new_warning['level'] = warning.w_level
            new_warning['msg'] = warning.w_msg
            new_warning['time'] = warning.w_time
            newRouter['warnings'].append(new_warning)
    return jsonify(newRouter), 200

@developPanel.route("/Router/<id>/Stop", methods=['GET'])
@authenticator.requires_dev_admin
def RouterStop(id=None):
    send_message(id,"SHTDWN")
    return jsonify({'status':'Shutting Down'}), 200

@developPanel.route("/Router/<id>/Restart", methods=['GET'])
@authenticator.requires_dev_admin
def RouterRestart(id=None):
    send_message(id,"RSTART")
    return jsonify({'status':'Restarting'}), 200

@developPanel.route("/Router/<id>/SleepPhotons", methods=['GET'])
@authenticator.requires_dev_admin
def RouterSleep(id=None):
    send_message(id,"SLPPHN")
    return jsonify({'status':'Sleeping Photons'}), 200

@developPanel.route("/Server/", methods=['GET'])
@authenticator.requires_dev_admin
def Server(id=None):
    db = DatabaseHandler()
    router_warnings = db.getRouterWarnings("The Server")
    newRouter = {}
    newRouter['name'] = "The Server"
    newRouter['lastOnline'] = round(time.time())
    newRouter['warnings'] = []
    for warning in router_warnings[:20]:
            new_warning = {}
            new_warning['level'] = warning.w_level
            new_warning['msg'] = warning.w_msg
            new_warning['time'] = warning.w_time
            newRouter['warnings'].append(new_warning)
    return jsonify(newRouter), 200

@developPanel.route("/Server/Stop", methods=['GET'])
@authenticator.requires_dev_admin
def ServerStop():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return jsonify({'status':'Shutting Down'}), 200

@developPanel.route("/Server/Restart", methods=['GET'])
@authenticator.requires_dev_admin
def ServerRestart():
        func = request.environ.get('werkzeug.server.restart')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return jsonify({'status':'Restarting'}), 200