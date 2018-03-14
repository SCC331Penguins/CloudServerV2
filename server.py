from flask import Flask
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database.database import db
from routes.debug import debug
from routes.user import user
from routes.api import api
from routes.router import router_route
from routes.sensor import sensor_route
from routes.admin import admin_route
from routes.historic import historic
import logging
import config

logger = logging.getLogger()
fhandler = logging.FileHandler(filename='mylog.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)


def create_app():
    logger.info("Creating Flask init_app")
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    CORS(app, resources=r"/*")
    db.init_app(app)
    flask_admin = Admin(app)
    with app.test_request_context():
        from database.models import Users, Router, Sensor
        flask_admin.add_view(ModelView(Users, db.session))
        flask_admin.add_view(ModelView(Router, db.session))
        flask_admin.add_view(ModelView(Sensor, db.session))
        register_blueprints(app)
        db.create_all()
        from MQTT.mqtt_client import client
        from handlers.database_handler import DatabaseHandler
        channels = DatabaseHandler().get_router_channels()
        for ch in channels[:]:
            client.subscribe(ch)
            print("MQTT: Subscribing to: " + str(ch))
        client.loop_start()
    return app


def register_blueprints(app):
    logger.info("Registering Blueprints")
    app.register_blueprint(debug)
    app.register_blueprint(user)
    app.register_blueprint(api)
    app.register_blueprint(router_route)
    app.register_blueprint(sensor_route)
    app.register_blueprint(admin_route)
    app.register_blueprint(historic)


app = create_app()

if __name__ == '__main__':
    logger.info("Starting Flask Server")
    app.run(debug=True, host=config.IP,
            port=5001, threaded=True, use_reloader=False)
