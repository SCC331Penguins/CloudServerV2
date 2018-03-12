

class MessageCreator():

    INIT_ROUTER = 1
    UPDATE_SENSORS = "UPDSEN"
    ACTIVE_SENSORS = "ACTSEN"
    SET_WIFI_CREDS = "WIFICR"
    UPDATE_SCRIPT = "UPDSCR"
    PING = "PING"
    SAVE_DATA = "DATA"
    NEW_CHANNEL = "NCHAN"
    REG_ACTUATOR = "REGACT"
    NOTIFICATION = "NOTIF"
    COMMAND = "COM"
    CONFIG_BUTTON = "CONFIB"
    PHONE_LOCATION = "PHOLOC"
    ARM_SYSTEM = "ARM"

    def __init__(self, type, payload):
        self.type = type
        self.payload = payload
        self.message = {}
        self.serialize()

    def serialize(self):
        self.message.update({'token': 0})
        self.message.update({"type": self.type})
        self.message.update({"payload": self.payload})
        return self.message

    def __repr__(self):
        return '<MQTT Type: ' + str(self.type) + ', Payload: ' + str(self.payload) + '>'
