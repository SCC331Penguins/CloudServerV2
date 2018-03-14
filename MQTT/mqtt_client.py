import paho.mqtt.client as mqtt
import json
import config
import logging
from datetime import datetime
import calendar
from handlers.message_handler import MessageHandler

logger = logging.getLogger()


def on_message(client, userdata, message):
    topic = message.topic
    if (message.topic in config.ADMIN_CHANNELS) is True:
        return
    print()
    message = json.loads(str(message.payload)[2:-1])
    mess = MessageHandler(message)
    res = mess.perform()
    if res is not None:
        print("OI OI " + str(res.payload))
        send_message(topic, res)
    if config.DEBUG is True and mess.id is not False:
        print(mess)


def on_connect(client, flags, userdata, rc):
    print("Connected to MQTT Broker: ")
    logger.info("Connected to MQTT Broker")


def send_message(topic, payload):
    logger.info("Sending Message: " + str(payload) + " to topic: " + str(topic))
    if config.DEBUG_MQTT is True:
        print("<Topic: " + topic + ", " + str(payload))
        print(payload.message)
    client.publish(topic, json.dumps(payload.message))


def open_admin_link(topic_name, user):
    config.ADMIN_CHANNELS.append(topic_name)
    if user in config.ADMIN_ASSIGNED_CHANNELS.keys():
        print("Updating keys before: " + str(config.ADMIN_CHANNELS))
        config.ADMIN_CHANNELS.remove(config.ADMIN_ASSIGNED_CHANNELS[user])
        print("Updating keys after : " + str(config.ADMIN_CHANNELS))
    config.ADMIN_ASSIGNED_CHANNELS.update({user: topic_name})
    print(config.ADMIN_ASSIGNED_CHANNELS)
    client.subscribe(topic_name)


def close_admin_link(topic_name):
    config.ADMIN_CHANNELS.remove(topic_name)
    client.unsubscribe(topic_name)

def send_router_update(router, remove=None):
    if remove is None:
        return
    if remove is False:
        payload = {"type": "ROUTERUPDADD"}
        dic = {'router_id': router, 'sensors': 0, 'owner': None, 'online': False, 'last_heard': 0}
        payload.update(dic)
    else:
        payload = {"type": "ROUTERUPDREM"}
        dic = {'router_id': router}
        payload.update(dic)
    if config.DEBUG_MQTT is True:
        print(payload)
    for channel in config.ADMIN_CHANNELS[:]:
        client.publish(channel, json.dumps(payload))


def send_sensor_update(sensor_id, remove=None):
    if remove is None:
        return
    if remove is False:
        payload = {"type": "SENSORUPDADD"}
        dic = {"sensor_id": sensor_id, "config": 0, "router": None}
        payload.update(dic)
    else:
        payload = {"type": "SENSORUPDREM"}
        dic = {"sensor_id": sensor_id}
        payload.update(dic)
    if config.DEBUG_MQTT is True:
        print(payload)
    for channel in config.ADMIN_CHANNELS[:]:
        client.publish(channel, json.dumps(payload))


def send_user_update(username, remove=None, id=None):
    if remove is None:
        return
    if remove is False:
        payload = {"type": "USERUPDADD", "username": username, "id": id}
    else:
        payload = {"type": "USERUPDREM", "username": username}
    if config.DEBUG_MQTT is True:
        print(payload)
    for channel in config.ADMIN_CHANNELS[:]:
        client.publish(channel, json.dumps(payload))
        

def send_admin_update(username, admin):
    payload = {"type": "USERUPDADM", "username": username, "admin": admin}
    if config.DEBUG_MQTT is True:
        print(payload)
    for channel in config.ADMIN_CHANNELS[:]:
        client.publish(channel, json.dumps(payload))


def send_message_admin(type, info):
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    payload = {"type": "ADMINDATA", "timestamp": unixtime, "action": type, "info": info}
    if config.DEBUG_MQTT is True:
        print(payload)
    for channel in config.ADMIN_CHANNELS[:]:
        client.publish(channel, json.dumps(payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(config.IP, 1883)
