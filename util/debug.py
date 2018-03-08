from functools import wraps
import config
from flask import request


class Request():

    def __init__(self, flask_request, path, short=False):
        self.request = flask_request.json.copy()
        self.id = self.request.get('token', None)
        if self.id is not None:
            del self.request['token']
        self.path = path
        self.short = short
        pass

    def __repr__(self):
        if len(self.request) == 0:
            return '<'+str(request.method)+', Path: '+str(self.path)+', ID: '+str(self.id)+'>'
        if self.short is False:
            return '<'+str(request.method)+', Path:  '+str(self.path)+', ID: '+str(self.id)+", Payload: "+str(
                self.request)+'>'
        return '<'+str(request.method)+', Path:  '+str(self.path)+', ID: '+str(self.id)+", Payload Len: "+str(
            len(self.request))+'>'


def print_request(f):
    @wraps(f)
    def print_req(*args, **kwargs):
        if config.DEBUG is True:
            print(Request(request, request.url_rule))
        return f(*args, **kwargs)
    return print_req


def print_request_short(f):
    @wraps(f)
    def print_req(*args, **kwargs):
        if config.DEBUG is True:
            print(Request(request, request.url_rule, short=True))
        return f(*args, **kwargs)
    return print_req
