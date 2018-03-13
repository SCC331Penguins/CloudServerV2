import sqlite3
import config
import time

"""
MQTT DATABASE HANDLER
Copy and paste from the scc-ug331
"""


# Database Handler for MQTT
class DatabaseHandler():

    def __init__(self):
        self.connection = sqlite3.connect(config.DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def register_ping(self, router_id):
        self.execute_query(
            "UPDATE Router SET last_heard = "+str(int(time.time())) + " WHERE router_id = '"+str(router_id)+"'")

    def get_phone_token(self, router_id):
        return self.fetch_result(self.execute_query("SELECT token FROM phone_token WHERE router_id = '"+str(router_id)+"'"))

    def init_sensor(self, sensor_id, router_id):
        checkSensorExists = "SELECT sensor_id FROM Sensor WHERE sensor_id = \"" + str(sensor_id) + "\""
        result = self.fetch_result(self.execute_query(checkSensorExists))
        if len(result) == 0:
            self.execute_query("INSERT INTO Sensor VALUES (\""+str(sensor_id)+"\", 0)")
        findSensor = "SELECT sensor_id FROM router_sensors WHERE sensor_id = \"" + str(sensor_id) + "\""
        result = self.fetch_result(self.execute_query(findSensor))
        if len(result) >= 1:
            q = "UPDATE router_sensors SET router_id = \""+str(router_id)+"\" WHERE sensor_id = \""+str(sensor_id)+"\""
        else:
            q = "INSERT INTO router_sensors VALUES (\""+str(router_id)+"\", \""+str(sensor_id)+"\")"
        self.execute_query(q)

    def get_rooms(self, router_id):
        result = self.fetch_result(self.execute_query("SELECT sensor_id FROM router_sensors WHERE router_id = \""+str(router_id)+"\""))
        if len(result) == 0:
            return []
        list_of_rooms = []
        for res in result[:]:
            room_res = self.fetch_result(self.execute_query("SELECT room FROM sensor_rooms WHERE sensor_id = \""+str(res[0])+"\""))
            if len(room_res) == 0:
                return []
            sensor_room = {"id": res[0], "room": room_res[0][0]}
            list_of_rooms.append(sensor_room)
        return list_of_rooms

    def record_reading(self, timestamp, router_id, data):
        sensor_id = data['id']
        temperature = data['temperature']
        humidity = data['humidity']
        movement = data['movement']
        light = data['light']
        sound = data['sound']
        uv = data['uv']
        ir = data['ir']

        if temperature != "null":
            self.execute_query("INSERT INTO temperature"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(temperature)+")")
        if humidity != "null":
            self.execute_query("INSERT INTO humidity"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(humidity)+")")
        if light != "null":
            self.execute_query("INSERT INTO light"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(light)+")")
        if movement != "null":
            self.execute_query("INSERT INTO movement"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(movement)+")")
        if sound != "null":
            self.execute_query("INSERT INTO sound"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(sound)+")")
        if uv != "null":
            self.execute_query("INSERT INTO uv"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(uv)+")")
        if ir != "null":
            self.execute_query("INSERT INTO ir"
            "(router_id, sensor_id, timestamp, value) VALUES ( '"+str(router_id)+"', '"+str(sensor_id)+"', "+str(timestamp)+", "+str(ir)+")")

    def get_reading(self, router_id, sensor_id=None, start=None, end=None):
        if sensor_id is None:
            pass

        time_restric = ""

        "1519664178 and 1519748511"

        if start is not None and end is not None:
            time_restric = " AND timestamp BETWEEN " + str(start) + " AND " + str(end)

        data = {}
        result = {}
        list = []

        temperature = self.fetch_result(self.execute_query("SELECT timestamp, value FROM temperature WHERE sensor_id = '"+str(sensor_id)+"'" + time_restric))
        data.update({"temperature": temperature})
        humidity = self.fetch_result(self.execute_query("SELECT timestamp, value FROM humidity WHERE sensor_id = '"+str(sensor_id)+"'" + time_restric))
        data.update({"humidity": humidity})
        light = self.fetch_result(self.execute_query("SELECT timestamp, value FROM light WHERE sensor_id = '"+str(sensor_id)+"'" + time_restric))
        data.update({"light": light})
        movement = self.fetch_result(self.execute_query("SELECT timestamp, value FROM movement WHERE sensor_id = '"+str(sensor_id)+"'" + time_restric))
        data.update({"movement": movement})
        sound = self.fetch_result(self.execute_query("SELECT timestamp, value FROM sound WHERE sensor_id ='"+str(sensor_id)+"'" + time_restric))
        data.update({"sound": sound})
        uv = self.fetch_result(self.execute_query("SELECT timestamp, value FROM uv WHERE sensor_id = '"+str(sensor_id)+"'" + time_restric))
        data.update({"uv": uv})
        ir = self.fetch_result(self.execute_query("SELECT timestamp, value FROM ir WHERE sensor_id = '"+str(sensor_id)+"'" + time_restric))
        data.update({"ir": ir})
        list.append(data)
        result.update({"data": list})
        return result

    def execute_query(self, query):
        result = []
        try:
            result = self.cursor.execute(query)
        except Exception as e:
            print(e)
            result = 0
        self.save()
        return result

    def save(self):
        self.connection.commit()

    def close(self):
        self.cursor = None
        self.connection.close()

    @staticmethod
    def fetch_result(result):
        result_array = []
        while True:
            fetched_result = result.fetchone()
            if fetched_result is None:
                break
            result_array.append(fetched_result)
        return result_array
