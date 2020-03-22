from validator.query_request_validator import QueryRequestValidator
from constants.request_parameters import QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE, QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE
from constants.database import MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD, MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD
from constants.response_messages import ERROR_QUERY_TYPE_REQUIRED, ERROR_DOMAIN_REQUIRED, ERROR_USERNAME_SPECIFIED_BUT_BLANK
from utils.test import create_mock_request, create_mock_dbclient_with_master_collection


def test_query_request_validator_incorrect_query_type():
    """Tests the QueryRequestValidator class with unacceptable query type.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  query_type='-1',
                                  domain='some_domain')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = QueryRequestValidator(
        request, dbclient, acceptable_query_type=[]).isValid()
    assert valid == False
    assert message == ERROR_QUERY_TYPE_REQUIRED


def test_query_request_validator_domain_missing():
    """Tests the QueryRequestValidator class with domain missing.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  query_type=QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE)
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = QueryRequestValidator(request, dbclient,
                                           acceptable_query_type=[
                                               QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE,
                                               QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE
                                           ]).isValid()
    assert valid == False
    assert message == ERROR_DOMAIN_REQUIRED


def test_query_request_validator_valid_request():
    """Tests the QueryRequestValidator class with valid request.
    Expects validation success and no error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  query_type=QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE,
                                  domain='some_domain')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = QueryRequestValidator(request, dbclient,
                                           acceptable_query_type=[
                                               QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE,
                                               QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE
                                           ]).isValid()
    assert valid == True
    assert message == None


def test_query_request_validator_username_present_but_empty():
    """Tests the QueryRequestValidator class with empty username.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  query_type=QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE,
                                  domain='some_domain',
                                  username='')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = QueryRequestValidator(request, dbclient,
                                           acceptable_query_type=[
                                               QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE,
                                               QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE
                                           ]).isValid()
    assert valid == False
    assert message == ERROR_USERNAME_SPECIFIED_BUT_BLANK


def test_query_request_validator_username_present_and_non_empty():
    """Tests the QueryRequestValidator class with valid request having non-empty username.
    Expects validation success and no error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  query_type=QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE,
                                  domain='some_domain',
                                  username='some_username')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = QueryRequestValidator(request, dbclient,
                                           acceptable_query_type=[
                                               QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE,
                                               QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE
                                           ]).isValid()
    assert valid == True
    assert message == None
