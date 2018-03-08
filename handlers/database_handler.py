from database.database import db
from passlib.apps import custom_app_context as pwd_context
from util.auth import authenticator
import time

"""
FLASK DATABASE HANDLER
"""
# TODO Add histroic data
# TODO Refactor Android device
# TODO Add NOTIFICATION support
# TODO Add phone token support


# DatabaseHandler
class DatabaseHandler():

        def __init__(self):
            from database.models import (Users, Router, UserRouters,
                                         RouterSensors, Sensor, Actuator,
                                         Script, PhoneToken)
            self.Users = Users
            self.Router = Router
            self.UserRouters = UserRouters
            self.Actuators = Actuator
            self.RouterSensors = RouterSensors
            self.Sensor = Sensor
            self.Script = Script
            self.PhoneToken = PhoneToken
            pass

        # Get user routers
        def get_user_routers(self, id):
            routers = db.session.query(self.UserRouters).filter(self.UserRouters.user_id == id).all()
            if self.check_result(routers) is None:
                return []
            return_result = []
            for x in routers[:]:
                rl = []
                rl.append(x.router_id)
                rl.append(self.get_router_status(x.router_id))
                return_result.append(rl)
            return return_result

        # Get a routers sensors
        def get_router_sensors(self, router_id):
            if self.router_exists(router_id) is False:
                return False
            res = db.session.query(self.RouterSensors, self.Sensor).filter(
                self.RouterSensors.sensor_id == self.Sensor.sensor_id).filter(
                    self.RouterSensors.router_id == router_id).all()
            ret = []
            for x in res[:]:
                sensor = []
                sensor.append(x[1].sensor_id)
                sensor.append(x[1].config)
                ret.append(sensor)
            return ret

        def set_phone_token(self, token, router_id):
            res = db.session.query(self.PhoneToken.router_id == router_id).all()
            db.session.remove(res)
            db.session.commit()
            self.add(self.PhoneToken(token, router_id))

        # Add a script to the database
        def add_script(self, router_id, script):
            if self.router_exists(router_id) is False:
                return False
            res = db.session.query(self.Script).filter(self.Script.script == script).first()
            if res is not None:
                return False
            self.add(self.Script(router_id, script))
            return True

        # Get scripts from database
        def get_script(self, router_id=None, script_id=None):
            if router_id is None and script_id is not None:
                return db.session.query(self.Script).filter(self.Script.script_id == script_id).first()
            if router_id is not None and script_id is None:
                return db.session.query(self.Script).filter(self.Script.router_id == router_id).all()
            return None

        # Update sensor Config
        def set_sensor_config(self, sensor_id, config):
            db.session.query(self.Sensor).filter(self.Sensor.sensor_id == sensor_id).update({"config": config})
            db.session.commit()
            pass

        # Register User
        def register_user(self, username, password):
            if self.user_exists(username=username):
                return False
            password = pwd_context.encrypt(password)
            self.add(self.Users(username, password))
            return True

        # Login User
        def login_user(self, username, password):
            if self.user_exists(username=username) is False:
                return [(False, "User does not exist")]
            user = self.get_user(username)
            if pwd_context.verify(password, user.password) is True:
                return [(True, authenticator.generate_token(user.id))]
            return [(False, "Incorrect password")]

        # Get the user by their username
        def get_user(self, username):
            return db.session.query(self.Users).filter(self.Users.username == username).first()

        def get_router(self, router_id):
            return db.session.query(self.Router).filter(self.Router.router_id == router_id).first()

        # Check if router exists
        def router_exists(self, router_id):
            r = db.session.query(self.Router).filter(self.Router.router_id == router_id).first()
            if r is None:
                return False
            return True

        # Check if user has claimed router
        def user_has_router(self, router_id, user_id):
            if self.router_exists(router_id) is False:
                return False
            c = db.session.query(self.UserRouters).filter(
                self.UserRouters.router_id == router_id and
                self.UserRouters.user_id == user_id).first()
            if c is None:
                return False
            return True

        # Claim Router
        def claim_router(self, router_id, user_id):
            if self.router_exists(router_id) is False:
                return False
            r = db.session.query(self.UserRouters).filter(self.UserRouters.router_id == router_id).first()
            if r is not None:
                return False
            self.add(self.UserRouters(router_id, user_id))
            return True

        # Check if router pinged last 2 mins
        def get_router_status(self, router_id):
            r = db.session.query(self.Router).filter(self.Router.router_id == router_id).first()
            time_now = int(time.time())
            if (time_now - r.last_heard) < 120:
                return True
            return False

        # Get router channels to open for mqtt
        def get_router_channels(self):
            r = db.session.query(self.Router).all()
            routers = []
            for x in r[:]:
                routers.append(x.router_id)
            return routers

        def get_actuators(self, router_id):
            r = db.session.query(self.Actuators).filter(self.Actuators.router_id == router_id).all()
            actuators = []
            for x in r[:]:
                actuator = []
                actuator.append(x.actuator_id)
                actuator.append(x.type)
                actuator.append(x.functions)
                actuators.append(actuator)
            return actuators

        # check if user exists
        def user_exists(self, id=None, username=None):
            if id is not None and username is None:
                user = db.session.query(self.Users).filter(self.Users.id == id).first()
            if username is not None and id is None:
                user = db.session.query(self.Users).filter(self.Users.username == username).first()
            if user is None:
                return False
            return True

        # Check multiple query result
        def check_result(self, result):
            if len(result) == 0:
                return None
            return result

        def add(self, model):
            db.session.add(model)
            db.session.commit()
