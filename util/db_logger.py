import logging
from handlers.database_handler import DatabaseHandler
class DBLogger(logging.StreamHandler):
    on_same_line = False
    level = logging.DEBUG
    def emit(self, record):
        try:
            rec = {
                "time":record.asctime,
                "level":record.levelno,
                "message":"%(message)s @ [%(pathname)s(%(lineno)d)]" % {"message":record.message, "pathname":record.pathname, "lineno":record.lineno}
            }
            DatabaseHandler().add_warning_record(rec, "SERVER", "The Server")
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
