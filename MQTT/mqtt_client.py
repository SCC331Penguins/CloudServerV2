import paho.mqtt.client as mqtt
import json
import config
import logging
from datetime import datetime
import calendar
from handlers.message_handler import MessageHandler

logger = logging.getLogger()


def on_message(client, userdata, message):
    if (message.topic in config.ADMIN_CHANNELS) is True:
        return
    message = json.loads(message.payload)
    mess = MessageHandler(message)
    if config.DEBUG is True and mess.id is not False:
        print(mess)


def on_connect(client, flags, userdata, rc):
    print("Connected to MQTT Broker: ")
    logger.info("Connected to MQTT Broker")


def send_message(topic, payload):
    logger.info("Sending Message: " + str(payload) + " to topic: " + str(topic))
    if config.DEBUG_MQTT is True:
        print(payload)
    client.publish(topic, json.dumps(payload.message))


def open_admin_link(topic_name):
    config.ADMIN_CHANNELS.append(topic_name)
    client.subscribe(topic_name)


def close_admin_link(topic_name):
    config.ADMIN_CHANNELS.remove(topic_name)
    client.unsubscribe(topic_name)


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
