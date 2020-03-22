from constants.response_messages import VALID_UPDATE_COMMAND, INVALID_REQUEST_RESPONSE_CODE
from flask import abort
from flask import request
from functools import wraps
from validator.update_request_validator import UpdateRequestValidator


def validate_update_request(dbclient):
    def validate_update(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            valid, message = UpdateRequestValidator(
                request, dbclient).isValid()
            if not valid:
                abort(INVALID_REQUEST_RESPONSE_CODE,
                      '{}\n{}'.format(message, VALID_UPDATE_COMMAND))
            else:
                return f(*args, **kwargs)
        return wrap
    return validate_update
