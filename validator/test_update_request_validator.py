from validator.update_request_validator import UpdateRequestValidator
from constants.database import MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD, MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD
from constants.response_messages import ERROR_DOMAIN_REQUIRED, ERROR_USERNAME_SPECIFIED_BUT_BLANK, ERROR_NEW_USERNAME_SPECIFIED_BUT_BLANK, ERROR_NEW_SECRET_SPECIFIED_BUT_BLANK, ERROR_OLD_AND_NEW_USERNAME_SAME, ERROR_DUPLICATE_DOMAIN_NEW_USERNAME, ERROR_SINGLE_RECORD_MATCH_REQUIRED_FOR_UPDATE
from utils.test import create_mock_request, create_mock_dbclient_with_master_collection, create_mock_dbclient_with_master_and_password_manager_collection, create_mock_dbclient_with_master_and_multiple_password_manager_collection


def test_update_request_validator_domain_missing():
    """Tests the UpdateRequestValidator class with domain missing.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = UpdateRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_DOMAIN_REQUIRED


def test_update_request_validator_username_present_but_empty():
    """Tests the UpdateRequestValidator class with empty username.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  username='')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = UpdateRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_USERNAME_SPECIFIED_BUT_BLANK


def test_update_request_validator_new_username_present_but_empty():
    """Tests the UpdateRequestValidator class with empty new username.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  new_username='')
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = UpdateRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_NEW_USERNAME_SPECIFIED_BUT_BLANK


def test_update_request_validator_new_secrets_present_but_invalid():
    """Tests the UpdateRequestValidator class with invalid secrets.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  new_secret=['some_Secret', None])
    dbclient = create_mock_dbclient_with_master_collection(master_password='abcd',
                                                           master_key='1234')
    valid, message = UpdateRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_NEW_SECRET_SPECIFIED_BUT_BLANK


def test_update_request_validator_same_old_and_new_username():
    """Tests the UpdateRequestValidator class with same old and new username.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  new_username='some_username')
    dbclient = create_mock_dbclient_with_master_and_password_manager_collection(master_password='abcd',
                                                                                master_key='1234',
                                                                                domain='some_domain',
                                                                                username='some_username')
    valid, message = UpdateRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_OLD_AND_NEW_USERNAME_SAME


def test_update_request_validator_no_record_match():
    """Tests the UpdateRequestValidator class with domain that doesn't exists in password manager collection.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain')
    dbclient = create_mock_dbclient_with_master_and_password_manager_collection(master_password='abcd',
                                                                                master_key='1234',
                                                                                domain=None,
                                                                                username=None)
    valid, message = UpdateRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_SINGLE_RECORD_MATCH_REQUIRED_FOR_UPDATE


def test_update_request_validator_domain_and_new_username_already_exists():
    """Tests the UpdateRequestValidator class with domain and new username combination already existing in the password manager collection.
    Expects validation failure and correct error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  new_username='some_new_username')
    dbclient = create_mock_dbclient_with_master_and_multiple_password_manager_collection(master_password='abcd',
                                                                                         master_key='1234',
                                                                                         domain1='some_domain',
                                                                                         username1='some_username',
                                                                                         domain2='some_domain',
                                                                                         username2='some_new_username')
    valid, message = UpdateRequestValidator(request, dbclient).isValid()
    assert valid == False
    assert message == ERROR_DUPLICATE_DOMAIN_NEW_USERNAME


def test_update_request_validator_valid_request():
    """Tests the UpdateRequestValidator class with a valid request.
    Expects validation success and no error message."""

    request = create_mock_request(master_password='abcd',
                                  master_key='1234',
                                  domain='some_domain',
                                  username='some_username',
                                  new_username='some_new_username',
                                  secret=['some_secret'])
    dbclient = create_mock_dbclient_with_master_and_multiple_password_manager_collection(master_password='abcd',
                                                                                         master_key='1234',
                                                                                         domain1='some_domain',
                                                                                         username1='some_username',
                                                                                         domain2=None,
                                                                                         username2=None)
    valid, message = UpdateRequestValidator(request, dbclient).isValid()
    assert valid == True
    assert message == None
