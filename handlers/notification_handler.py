from pyfcm import FCMNotification
from MQTT.database_handler import DatabaseHandler
import config


def send_notification(router_id, data_message):
    dm = {'message': data_message}
    push_service = FCMNotification(api_key=config.FCM_SERVER_API)
    db = DatabaseHandler()
    token = db.get_phone_token(router_id)
    phones = []
    for x in token[:]:
        print(x[0])
        phones.append(x[0])
    result = push_service.notify_multiple_devices(registration_ids=phones, data_message=dm)
    print(result)
