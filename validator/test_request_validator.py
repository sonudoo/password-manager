import pytest
from validator.request_validator import RequestValidator
from constants.request_parameters import BODY_MASTER_KEY_PARAM, BODY_MASTER_PASSWORD_PARAM
from constants.database import MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD, MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD
from utils.test import create_mock_request, create_mock_dbclient, create_mock_dbclient_with_master_collection


def test_request_validator_master_password_missing():
    """Tests the RequestValidator class with missing master password.
    Expects error thrown."""

    request = create_mock_request(master_key='1234')
    dbclient = create_mock_dbclient()
    with pytest.raises(AssertionError):
        RequestValidator(request, dbclient).isValid()


def test_request_validator_master_key_missing():
    """Tests the RequestValidator class with missing master key.
    Expects error thrown."""

    request = create_mock_request(master_password='abcd')
    dbclient = create_mock_dbclient()
    with pytest.raises(AssertionError):
        RequestValidator(request, dbclient).isValid()


def test_request_validator_incorrect_master_password():
    """Tests the RequestValidator class with incorrect master password.
    Expects error thrown."""

    request = create_mock_request(master_password='dcba',
                                  master_key='1234')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    with pytest.raises(AssertionError):
        RequestValidator(request, dbclient).isValid()


def test_request_validator_incorrect_master_key():
    """Tests the RequestValidator class with incorrect master password.
    Expects error thrown."""

    request = create_mock_request(master_password='abcd',
                                  master_key='4321')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    with pytest.raises(AssertionError):
        RequestValidator(request, dbclient).isValid()


def test_request_validator_correct_credentials():
    """Tests the RequestValidator class with a valid request.
    Expects validation success and no error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    RequestValidator(request, dbclient).isValid()
