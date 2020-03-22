from constants.response_messages import VALID_INSERT_COMMAND, INVALID_REQUEST_RESPONSE_CODE
from flask import abort
from flask import request
from functools import wraps
from validator.insert_request_validator import InsertRequestValidator


def validate_insert_request(dbclient):
    def validate_insert(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            valid, message = InsertRequestValidator(
                request, dbclient).isValid()
            if not valid:
                abort(INVALID_REQUEST_RESPONSE_CODE,
                      '{}\n{}'.format(message, VALID_INSERT_COMMAND))
            else:
                return f(*args, **kwargs)
        return wrap
    return validate_insert
