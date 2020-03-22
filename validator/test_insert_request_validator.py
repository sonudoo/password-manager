from validator.insert_request_validator import InsertRequestValidator
from constants.request_parameters import QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE, QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE
from constants.database import MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD, MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD
from constants.response_messages import ERROR_DOMAIN_REQUIRED, ERROR_USERNAME_REQUIRED, ERROR_SECRETS_REQUIRED, ERROR_ATLEAST_ONE_SECRET_REQUIRED, ERROR_DUPLICATE_DOMAIN_USERNAME
from utils.test import create_mock_request, create_mock_dbclient_with_master_collection, create_mock_dbclient_with_master_and_password_manager_collection


def test_insert_request_validator_domain_missing():
    """Tests the InsertRequestValidator class with missing domain. Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  username='some_username',
                                  secret=['some_secret'])
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = InsertRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_DOMAIN_REQUIRED


def test_insert_request_validator_username_missing():
    """Tests the InsertRequestValidator class with missing username. Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  secret=['some_secret'])
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = InsertRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_USERNAME_REQUIRED


def test_insert_request_validator_secrets_missing():
    """Tests the InsertRequestValidator class with secrets domain.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  username='some_username')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = InsertRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_ATLEAST_ONE_SECRET_REQUIRED


def test_insert_request_validator_secrets_invalid():
    """Tests the InsertRequestValidator class with invalid secrets.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  username='some_username',
                                  secret=['some_secret', None])
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = InsertRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_SECRETS_REQUIRED


def test_insert_request_validator_domain_username_already_exists():
    """Tests the InsertRequestValidator class with domain and username already existing in password manager collection.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  username='some_username',
                                  secret=['some_secret'])
    dbclient = create_mock_dbclient_with_master_and_password_manager_collection(master_password='abcd',
                                                                                master_key='1234',
                                                                                domain='some_domain',
                                                                                username='some_username')
    valid, message = InsertRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_DUPLICATE_DOMAIN_USERNAME


def test_insert_request_validator_valid_request():
    """Tests the InsertRequestValidator class with valid request.
    Expects validation success and no error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  username='some_username',
                                  secret=['some_secret'])
    dbclient = create_mock_dbclient_with_master_and_password_manager_collection(master_password='abcd',
                                                                                master_key='1234',
                                                                                domain=None,
                                                                                username=None)
    valid, message = InsertRequestValidator(request, dbclient).isValid()
    assert valid == True
    assert message == None
