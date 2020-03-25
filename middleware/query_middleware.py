from constants.response_messages import VALID_SEARCH_QUERY_TYPE_COMMAND, VALID_GET_SECRETS_QUERY_TYPE_COMMAND, INVALID_REQUEST_RESPONSE_CODE
from flask import abort
from flask import request
from functools import wraps
from validator.query_request_validator import QueryRequestValidator


def validate_query_request(dbclient):
    def validate_query(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            valid, message = QueryRequestValidator(request, dbclient).isValid()
            if not valid:
                return '{}\n{}\nOR\n{}'.format(
                    message, VALID_SEARCH_QUERY_TYPE_COMMAND, VALID_GET_SECRETS_QUERY_TYPE_COMMAND), INVALID_REQUEST_RESPONSE_CODE
            else:
                return f(*args, **kwargs)
        return wrap
    return validate_query
