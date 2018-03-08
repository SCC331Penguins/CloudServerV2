from database.database import db


class Temperature(db.Model):
    router_id = db.Column(db.String(30), primary_key=True)
    sensor_id = db.Column(db.String(100), primary_key=True)
    timestamp = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, primary_key=True)

    def __init__(self, router_id, sensor_id, timestamp, value):
        self.router_id = router_id
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = value


class Humidity(db.Model):
    router_id = db.Column(db.String(30), primary_key=True)
    sensor_id = db.Column(db.String(100), primary_key=True)
    timestamp = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, primary_key=True)

    def __init__(self, router_id, sensor_id, timestamp, value):
        self.router_id = router_id
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = value


class Light(db.Model):
    router_id = db.Column(db.String(30), primary_key=True)
    sensor_id = db.Column(db.String(100), primary_key=True)
    timestamp = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, primary_key=True)

    def __init__(self, router_id, sensor_id, timestamp, value):
        self.router_id = router_id
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = value


class Ir(db.Model):
    router_id = db.Column(db.String(30), primary_key=True)
    sensor_id = db.Column(db.String(100), primary_key=True)
    timestamp = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, primary_key=True)

    def __init__(self, router_id, sensor_id, timestamp, value):
        self.router_id = router_id
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = value


class Sound(db.Model):
    router_id = db.Column(db.String(30), primary_key=True)
    sensor_id = db.Column(db.String(100), primary_key=True)
    timestamp = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, primary_key=True)

    def __init__(self, router_id, sensor_id, timestamp, value):
        self.router_id = router_id
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = value


class Movement(db.Model):
    router_id = db.Column(db.String(30), primary_key=True)
    sensor_id = db.Column(db.String(100), primary_key=True)
    timestamp = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, primary_key=True)

    def __init__(self, router_id, sensor_id, timestamp, value):
        self.router_id = router_id
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = value


class Uv(db.Model):
    router_id = db.Column(db.String(30), primary_key=True)
    sensor_id = db.Column(db.String(100), primary_key=True)
    timestamp = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, primary_key=True)

    def __init__(self, router_id, sensor_id, timestamp, value):
        self.router_id = router_id
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = value
