from database.database import db

"""
Remember to run this on database change:
from server import db
db.create_all()
"""


# User Table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    is_admin = db.Column(db.Integer)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_admin = 0

    def __repr__(self):
        return '<User: %r>' % self.username


# Router Table
class Router(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    router_id = db.Column(db.String(20), unique=True)
    last_heard = db.Column(db.Integer)

    def __init__(self, router_id):
        self.router_id = router_id

    def __repr__(self):
        return '<Router: '+str(self.router_id)+', LP: '+str(self.last_heard)+'>'


# UserRouters Table
class UserRouters(db.Model):
    router_id = db.Column(db.String(20), db.ForeignKey(Router.router_id), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), primary_key=True)

    def __init__(self, router_id, user_id):
        self.router_id = router_id
        self.user_id = user_id

    def __repr__(self):
        return '<Router: '+str(self.router_id)+', User: '+str(self.user_id)+'>'


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.String(100), unique=True)
    config = db.Column(db.Integer, nullable=False)

    def __init__(self, sensor_id, config):
        self.sensor_id = sensor_id
        self.config = config

    def __repr__(self):
        return '<Sensor: '+str(self.sensor_id)+', Config: '+str(self.config)+'>'


class RouterSensors(db.Model):
    router_id = db.Column(db.String(20), db.ForeignKey(Router.router_id), primary_key=True)
    sensor_id = db.Column(db.String(100), db.ForeignKey(Sensor.sensor_id), primary_key=True)

    def __init__(self, router_id, sensor_id):
        self.router_id = router_id
        self.sensor_id = sensor_id

    def __repr__(self):
        return '<Router: '+str(self.router_id)+', Sensor: '+str(self.sensor_id)+'>'


class Actuator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    actuator_id = db.Column(db.String(20), unique=True)
    type = db.Column(db.String(20), nullable=False)
    functions = db.Column(db.Text, nullable=False)
    router_id = db.Column(db.String(20), db.ForeignKey(Router.router_id), nullable=False)

    def __init__(self, actuator_id, router_id, type, functions):
        self.actuator_id = actuator_id
        self.type = type
        self.functions = functions
        self.router_id = router_id

    def __repr__(self):
        return '<Actuator: '+str(self.type)+', ID: '+str(self.actuator_id)+', Router: '+str(self.router_id)+'>'


class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    router_id = db.Column(db.String, db.ForeignKey(Router.router_id), nullable=False)
    script = db.Column(db.Text, nullable=False, unique=True)

    def __init__(self, router_id, script):
        self.router_id = router_id
        self.script = script

    def __repr__(self):
        return '<Script ID: '+str(self.id)+', Router: '+str(self.router_id)+', Script: '+str(self.script)+'>'


class PhoneToken(db.Model):
    token = db.Column(db.String(100), primary_key=True)
    router_id = db.Column(db.String(30), db.ForeignKey(Router.router_id))

    def __init__(self, token, router_id):
        self.router_id = router_id
        self.token = token

    def __repr__(self):
        return '<PhoneToken: ' + str(self.token) + ', Router: ' + str(self.router_id) + '>'


db.create_all()
