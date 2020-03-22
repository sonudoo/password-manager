from auth.auth import Authenticator
from utils.test import create_mock_dbclient_with_auth_collection


def test_authenticator_auth_failed():
    """Tests for Authentication with invalid auth key, Expects authentication failure."""

    dbclient = create_mock_dbclient_with_auth_collection(key=None)
    assert Authenticator(dbclient).authenticate('some_key') == False


def test_authenticator_auth_success():
    """Tests for Authentication with valid auth key, Expects authentication success."""

    dbclient = create_mock_dbclient_with_auth_collection(key='some_key')
    assert Authenticator(dbclient).authenticate('some_key') == True
