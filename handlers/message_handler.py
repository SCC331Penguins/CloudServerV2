from util.auth.authenticator import verify_token
import logging
from MQTT.database_handler import DatabaseHandler
from handlers.message_creator import MessageCreator
from handlers.notification_handler import send_notification
from datetime import datetime
import calendar


logger = logging.getLogger()


def PING(message):
    print("PING From " + str(message.id))
    DatabaseHandler().register_ping(message.id)


def NOTIFICATION(message):
    send_notification(message.id, message.payload['message'])
    pass


def REG_ACTUATOR(message):
    pass


def SAVE_DATA(message):
    hh = DatabaseHandler()
    data = message.payload
    if len(data) == 0:
        return
    sensor_list = data['sensors']

    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())

    print(message)

    for s in sensor_list[:]:
        hh.record_reading(unixtime, message.id, s)


def ACTIVE_SENSORS(message):
    for sensor in message.payload[:]:
        DatabaseHandler().init_sensor(sensor, message.id)


def ROOM_REQUEST(message):
    print("ROOM REQ")
    print(message.id)
    sensors = DatabaseHandler().get_rooms(message.id)
    print(sensors)
    message_to_send = MessageCreator(MessageCreator.ROOM_RESPONSE, sensors)
    print("MESSAGE TO SEND" + str(message_to_send))
    return message_to_send

def SEND_LOG_DATA(message):
    print(message)
    DatabaseHandler().add_warning_record(message.payload, "Router", message.payload['R_id'])

# What to do with what type
typeDict = {
    MessageCreator.PING: PING,
    MessageCreator.NOTIFICATION: NOTIFICATION,
    MessageCreator.ACTIVE_SENSORS: ACTIVE_SENSORS,
    MessageCreator.REG_ACTUATOR: REG_ACTUATOR,
    # MessageCreator.SAVE_DATA: SAVE_DATA,
    MessageCreator.ROOM_REQUEST: ROOM_REQUEST,
    MessageCreator.SEND_LOG_DATA:SEND_LOG_DATA
}


class MessageHandler():

    def __init__(self, message):
        self.type = message['type']
        self.payload = message['payload']
        self.id = verify_token(message['token'])

    def perform(self):
        s = typeDict.get(self.type)
        print(self.payload)
        if s is not None:
            logger.debug("Message Received of type %s", self.type)
            return s(self)
        return None

    def __repr__(self):
        return '<ID: ' + str(self.id) + ', Type: ' + str(self.type) + ', Payload: ' + str(self.payload) + '>'
