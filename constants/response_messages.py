from constants.request_parameters import *

VALID_INSERT_COMMAND = 'Usage: curl <url>/insert -H "{}: (required)" -d "{}=(required)&{}=(required)&{}=(required)&{}=(required)&{}=(required)&{}=(optional)..."'.format(
    HEADERS_AUTH_KEY_PARAM, BODY_MASTER_PASSWORD_PARAM, BODY_MASTER_KEY_PARAM, BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM, BODY_SECRET_PARAM, BODY_SECRET_PARAM)
VALID_SEARCH_QUERY_TYPE_COMMAND = 'Usage: curl <url>/query -H "{}: (required)" -d "{}=1{}=(required)&{}=(required)&{}=(required)&{}=(optional)"'.format(
    HEADERS_AUTH_KEY_PARAM, BODY_QUERY_TYPE_PARAM, BODY_MASTER_PASSWORD_PARAM, BODY_MASTER_KEY_PARAM, BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM)
VALID_GET_SECRETS_QUERY_TYPE_COMMAND = 'Usage: curl <url>/query -H "{}: (required)" -d "{}=2&{}=(required)&{}=(required)&{}=(required)&{}=(optional)"'.format(
    HEADERS_AUTH_KEY_PARAM, BODY_QUERY_TYPE_PARAM, BODY_MASTER_PASSWORD_PARAM, BODY_MASTER_KEY_PARAM, BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM)
VALID_UPDATE_COMMAND = 'Usage: curl <url>/update -H "{}: (required)" -d "{}=(required)&{}=(required)&{}=(required)&{}=(optional)&{}=(optional)&{}=(optional)&{}=(optional)..."'.format(
    HEADERS_AUTH_KEY_PARAM, BODY_MASTER_PASSWORD_PARAM, BODY_MASTER_KEY_PARAM, BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM, BODY_NEW_USERNAME_PARAM, BODY_NEW_SECRET_PARAM, BODY_NEW_SECRET_PARAM)

ERROR_MASTER_PASSWORD = 'Master password is missing or incorrect.'
ERROR_MASTER_KEY = 'Master key is missing or incorrect.'
ERROR_MULTIPLE_MASTER_ROWS = 'Multiple master password/keys are available. Database is inconsistent.'
ERROR_DOMAIN_REQUIRED = 'Domain is missing in the request.'
ERROR_USERNAME_REQUIRED = 'Username is missing in the request.'
ERROR_ATLEAST_ONE_SECRET_REQUIRED = 'At least one secret is required.'
ERROR_SECRETS_REQUIRED = 'One or more secret(s) have missing values.'
ERROR_DUPLICATE_DOMAIN_USERNAME = 'The given combination of domain and username already exists.'
ERROR_QUERY_TYPE_REQUIRED = 'Query type is missing or invalid in request.'
ERROR_USERNAME_SPECIFIED_BUT_BLANK = 'If username is specified in request, then it should be non-empty.'
ERROR_MULTIPLE_RECORDS_FOUND_FOR_DECRYPTING_SECRETS = 'Multiple records were found. Only one record is allowed for decryption.'
ERROR_NO_RECORD_FOUND = 'No records were found for the given combination.'
ERROR_NEW_USERNAME_SPECIFIED_BUT_BLANK = 'If new username is specified in request, then it should be non-empty.'
ERROR_NEW_SECRET_SPECIFIED_BUT_BLANK = 'If new secrets is specified in request, then it should be valid.'
ERROR_SINGLE_RECORD_MATCH_REQUIRED_FOR_UPDATE = 'Exactly one record must match for update. Multiple or no match has been found.'
ERROR_OLD_AND_NEW_USERNAME_SAME = 'Old and new username cannot be same.'
ERROR_DUPLICATE_DOMAIN_NEW_USERNAME = 'The given combination for domain and new username already exists.'

SUCCESS = 'Success!'
UNAUTHORIZED = 'Unauthorized!'
INTERNAL_ERROR = 'Internal error!'
NOT_FOUND = 'Not found!'

SUCCESS_RESPONSE_CODE = 200
UNAUTHORIZED_RESPONSE_CODE = 403
INTERNAL_ERROR_RESPONSE_CODE = 500
NOT_FOUND_RESPONSE_CODE = 400
INVALID_REQUEST_RESPONSE_CODE = 400
