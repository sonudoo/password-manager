#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from auth.auth import Authenticator
from constants.database import MONGO_URI, DATABASE_NAME, \
    MASTER_PASSWORD_COLLECTION_NAME
from constants.request_parameters import HEADERS_AUTH_KEY_PARAM
from constants.response_messages import SUCCESS, UNAUTHORIZED, \
    INTERNAL_ERROR, NOT_FOUND, SUCCESS_RESPONSE_CODE, \
    INVALID_REQUEST_RESPONSE_CODE, UNAUTHORIZED_RESPONSE_CODE, \
    NOT_FOUND_RESPONSE_CODE, INTERNAL_ERROR_RESPONSE_CODE
from constants.url_paths import INSERT_PATH, QUERY_PATH, UPDATE_PATH
from database.dbclient import DbClient
from flask import Flask
from flask import request
from middleware.auth_middleware import auth_required
from middleware.insert_middleware import validate_insert_request
from middleware.query_middleware import validate_query_request
from middleware.update_middleware import validate_update_request
from processor.insert_processor import InsertProcessor
from processor.query_processor import QueryProcessor
from processor.update_processor import UpdateProcessor

dbclient = DbClient(mongo_uri=MONGO_URI, database=DATABASE_NAME)
app = Flask(__name__)


@app.route(INSERT_PATH, methods=['POST'])
@auth_required(dbclient)
@validate_insert_request(dbclient)
def insert():
    InsertProcessor(request, dbclient).process()
    return (SUCCESS, SUCCESS_RESPONSE_CODE)


@app.route(QUERY_PATH, methods=['POST'])
@auth_required(dbclient)
@validate_query_request(dbclient)
def query():
    try:
        result = QueryProcessor(request, dbclient).process()
        return (json.dumps(result, indent=2), SUCCESS_RESPONSE_CODE)
    except Exception as e:
        return (str(e.args), INVALID_REQUEST_RESPONSE_CODE)


@app.route(UPDATE_PATH, methods=['POST'])
@auth_required(dbclient)
@validate_update_request(dbclient)
def update():
    UpdateProcessor(request, dbclient).process()
    return (SUCCESS, SUCCESS_RESPONSE_CODE)


@app.errorhandler(UNAUTHORIZED_RESPONSE_CODE)
def api_unauthorized(error):
    return (UNAUTHORIZED, UNAUTHORIZED_RESPONSE_CODE)


@app.errorhandler(NOT_FOUND_RESPONSE_CODE)
def api_not_found(error):
    return (NOT_FOUND, NOT_FOUND_RESPONSE_CODE)


@app.errorhandler(500)
def api_internal_error(error):
    return (INTERNAL_ERROR, INTERNAL_ERROR_RESPONSE_CODE)


if __name__ == '__main__':
    app.run()
