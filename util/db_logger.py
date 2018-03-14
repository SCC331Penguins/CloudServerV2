import logging, time
import calendar
from MQTT.database_handler import DatabaseHandler
class DBLogger(logging.StreamHandler):
    on_same_line = False
    level = logging.DEBUG
    def emit(self, record):
        try:
            rec = {
                "level":str(record.levelno),
                "message":"%(message)s @ [%(pathname)s(%(lineno)d)]" % {"message": record.message, "pathname": record.pathname, "lineno": record.lineno},
                "time": str(calendar.timegm(time.strptime(record.asctime,"%Y-%m-%d %H:%M:%S,%f"))),
            }
            DatabaseHandler().add_warning_record(record=rec, originType="SERVER", originName="The Server")
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
