from auth.auth import Authenticator
from constants.request_parameters import HEADERS_AUTH_KEY_PARAM
from constants.response_messages import UNAUTHORIZED_RESPONSE_CODE
from flask import abort
from flask import request
from functools import wraps


def auth_required(dbclient):
    def auth_required_wrapper(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if request.headers.get(HEADERS_AUTH_KEY_PARAM) == None:
                abort(UNAUTHORIZED_RESPONSE_CODE)
            key = request.headers[HEADERS_AUTH_KEY_PARAM]
            if not Authenticator(dbclient).authenticate(key):
                abort(UNAUTHORIZED_RESPONSE_CODE)
            else:
                return f(*args, **kwargs)
        return wrap
    return auth_required_wrapper
