import paho.mqtt.client as mqtt
import json
import config
import logging
from handlers.message_handler import MessageHandler

logger = logging.getLogger()


def on_message(client, userdata, message):
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


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.110", 1883)
