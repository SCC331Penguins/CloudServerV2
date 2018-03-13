import jwt
import config
from functools import wraps
from flask import request, jsonify
from handlers.database_handler import DatabaseHandler


def generate_token(id):
    try:
        payload = {'id': id}
        return (jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")).decode('utf-8')
    except Exception as e:
        print(e)
        return


def verify_token(token):
    try:
        payload = jwt.decode(token, config.SECRET_KEY)
        return payload['id']
    except jwt.InvalidTokenError:
        return False


def requires_token(f):
    @wraps(f)
    def check(*args, **kwargs):
        id = verify_token(request.json['token'])
        if id is False:
            return jsonify(False), 404
        request.json['token'] = id
        return f(*args, **kwargs)
    return check


def requires_ownership(f):
    @wraps(f)
    def check(*args, **kwargs):
        res = DatabaseHandler().user_has_router(user_id=request.json['token'], router_id=request.json['router_id'])
        if res is False:
            return jsonify(False), 200
        return f(*args, **kwargs)
    return check


def requires_admin(f):
    @wraps(f)
    def admin(*args, **kwargs):
        id = verify_token(request.json['token'])
        if id is False:
            return jsonify(False), 200
        if DatabaseHandler().check_admin(id) is False:
            return jsonify(False), 200
        return f(*args, **kwargs)
    return admin
