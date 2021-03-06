from database.database import db
from passlib.apps import custom_app_context as pwd_context
from util.auth import authenticator
from sqlalchemy.exc import IntegrityError
import time
import json

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
                                         Script, PhoneToken, SensorRooms, RouterAuthUsers, Warnings)
            self.Users = Users
            self.Router = Router
            self.UserRouters = UserRouters
            self.Actuators = Actuator
            self.RouterSensors = RouterSensors
            self.Sensor = Sensor
            self.Script = Script
            self.PhoneToken = PhoneToken
            self.Rooms = SensorRooms
            self.RouterAuth = RouterAuthUsers
            self.Warnings = Warnings
            pass

        # Get user routers
        def get_user_routers(self, id):
            routers = db.session.query(self.UserRouters).filter(self.UserRouters.user_id == id).all()
            return_result = []
            authed_routers = self.get_authed_routers(id)
            print("Authed routers " + str(authed_routers))
            for x in routers[:]:
                rl = []
                rl.append(x.router_id)
                rl.append(self.get_router_status(x.router_id))
                return_result.append(rl)
            for x in authed_routers[:]:
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

        def check_admin(self, user_id):
            user = db.session.query(self.Users).get(user_id)
            if user is None:
                return False
            if user.is_admin == 0:
                return False
            return True

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
            user = self.Users(username, password)
            self.add(self.Users(username, password))
            id = len(db.session.query(self.Users).all())
            return {"id": id, "username": username}

        def save_rooms(self, router_id, sensors):
            for sensor in sensors[:]:
                db.session.query(self.Rooms).filter(self.Rooms.sensor_id == sensor['id']).delete()
                db.session.commit()
                self.add(self.Rooms(sensor['id'], sensor['room']))

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

        def get_user_from_id(self, id):
            user = db.session.query(self.Users).filter(self.Users.id == id).first()
            if user is None:
                return id
            return user.username

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
                self.UserRouters.user_id == user_id).all()
            if c is None:
                return False
            for r in c[:]:
                if r.router_id == router_id:
                    if r.user_id == user_id:
                        return True
            return False

        def get_sensors(self):
            sensors = db.session.query(self.Sensor).all()
            sensor_list = []
            for x in sensors[:]:
                res = self.get_sensors_router(x.sensor_id)
                dic = {'sensor_id': x.sensor_id, 'config': x.config, 'router': res}
                sensor_list.append(dic)
            return sensor_list

        def add_router(self, router_id):
            return self.add(self.Router(router_id))

        def add(self, model):
            db.session.add(model)
            try:
                db.session.commit()
            except IntegrityError as err:
                return False
            return True

        def set_user_admin(self, username, admin):
            user = db.session.query(self.Users).filter(self.Users.username == username).first()
            user.is_admin = admin
            db.session.commit()

        def get_users_admin(self):
            users = db.session.query(self.Users).all()
            if len(users) == 0:
                print("None")
                return []
            users_list = []
            for user in users[:]:
                print(user.username)
                routers = len(DatabaseHandler().get_user_routers(user.id))
                user_dict = {"id": user.id, "username": user.username, "is_admin": user.is_admin, "routers": routers}
                users_list.append(user_dict)
            return users_list

        def remove_router(self, router_id):
            db.session.query(self.Router).filter(self.Router.router_id == router_id).delete()
            db.session.commit()

        def remove_sensor(self, sensor_id):
            db.session.query(self.Sensor).filter(self.Sensor.sensor_id == sensor_id).delete()
            db.session.commit()

        def get_sensors_router(self, sensor_id):
            router = db.session.query(self.RouterSensors).filter(self.RouterSensors.sensor_id == sensor_id).first()
            if router is None:
                return None
            return router.router_id

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
            if r is None:
                return False
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

        # Get actuators
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

        def get_authed_users(self, router_id):
            result = db.session.query(self.RouterAuth).filter(self.RouterAuth.router_id == router_id).all()
            result_list = []
            for r in result[:]:
                username = self.get_user_from_id(r.user_id)
                result_list.append({"id": r.user_id, "username": username})
            return result_list

        def get_routers(self):
            routers = db.session.query(self.Router).all()
            if len(routers) == 0:
                return []
            router_list = []
            for x in routers[:]:
                res = self.get_router_sensors(x.router_id)
                res1 = self.get_router_owner(x.router_id)
                online = self.get_router_status(x.router_id)
                dic = {'router_id': x.router_id, 'sensors': len(res), 'owner': res1, 'online': online, 'last_heard': x.last_heard}
                router_list.append(dic)
            return router_list

        def add_sensor(self, sensor_id):
            return self.add(self.Sensor(sensor_id, 0))

        def remove_user(self, username):
            db.session.query(self.Users).filter(self.Users.username == username).delete()
            db.session.commit()

        def get_users(self):
            return db.session.query(self.Users).all()

        def is_sensor_claimed(self, sensor_id):
            result = db.session.query(self.RouterSensors).filter(self.RouterSensors.sensor_id == sensor_id).first()
            if result is None:
                return False
            return True

        def get_router_owner(self, router_id):
            router = db.session.query(self.UserRouters).filter(self.UserRouters.router_id == router_id).first()
            if router is None:
                return None
            user = db.session.query(self.Users).filter(self.Users.id == router.user_id).first()
            if user is None:
                return "Removed User"
            return user.username

        def get_authed_routers(self, user_id):
            authed_routers = db.session.query(self.RouterAuth).filter(self.RouterAuth.user_id == user_id).all()
            return authed_routers

        def user_has_auth(self, user_id, router_id):
            auth  = db.session.query(self.RouterAuth.router_id == router_id and self.RouterAuth.user_id == user_id).first()
            if auth is None:
                return False
            return True

        def remove_auth_user(self, user_id, router_id):
            auth = db.session.query(self.RouterAuth).filter(self.RouterAuth.router_id == router_id and self.RouterAuth.user_id == user_id).delete()
            db.session.commit()
            return True

        def add_auth_user(self, user_id, router_id):
            authed_user = self.RouterAuth(router_id, user_id)
            return self.add(authed_user)

        # Check multiple query result
        def check_result(self, result):
            if len(result) == 0:
                return None
            return result

        # ---Dev Panel
        def getAllRouters(self):
            return db.session.query(self.Router).all()

        def getAllRouterWarnings(self):
            return db.session.query(self.Warnings).filter(self.Warnings.originType == "Router").all()

        def getRouter(self, r_id):
            return db.session.query(self.Router).filter(self.Router.router_id == r_id).one()

        def getRouterWarnings(self, r_id):
            return db.session.query(self.Warnings).filter(self.Warnings.originName == r_id).all()
