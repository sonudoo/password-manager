from constants.request_parameters import BODY_MASTER_PASSWORD_PARAM, BODY_MASTER_KEY_PARAM
from constants.database import MASTER_PASSWORD_COLLECTION_NAME, MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD, MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD
from constants.response_messages import ERROR_MASTER_PASSWORD, ERROR_MASTER_KEY, ERROR_MULTIPLE_MASTER_ROWS
from utils.hash import generate_hash


class RequestValidator:
    """Base class for validation of master password and master key sent by the client.

    This class is extended by all the validators.
    isValid() of this class should be called to validate the master password and master key.

    Attributes:
        request (Request): Flask request object received from the client.
        master_password_collection (Collection): The collection in which master password and master key is stored.
    """
    request = None
    master_password_collection = None

    def __init__(self, request, dbclient):
        """
        Args:
            request (Request): The request object received from the client.
            dbclient (DbClient): The database client object.
        """
        self.request = request
        self.master_password_collection = dbclient.get_collection(
            MASTER_PASSWORD_COLLECTION_NAME)

    def isValid(self):
        """Asserts if the master password and master key are valid.
        The following validations are performed:

        1. Master password exists and is non-empty.
        2. Master key exists and is non-empty.
        3. The hash of master password and key is present in the master collection.
        """
        self.__assertMasterPasswordExists()
        self.__assertMasterKeyExists()
        self.__assertMasterPasswordAndKeyValid()

    def __assertMasterPasswordExists(self):
        """Asserts that the master password exists in request and is non-empty."""
        assert self.request.form.get(
            BODY_MASTER_PASSWORD_PARAM) != None, ERROR_MASTER_PASSWORD
        assert len(self.request.form.get(BODY_MASTER_PASSWORD_PARAM)
                   ) > 0, ERROR_MASTER_PASSWORD

    def __assertMasterKeyExists(self):
        """Asserts that the master key exists in request and is non-empty."""
        assert self.request.form.get(
            BODY_MASTER_KEY_PARAM) != None, ERROR_MASTER_KEY
        assert len(self.request.form.get(
            BODY_MASTER_KEY_PARAM)) > 0, ERROR_MASTER_KEY

    def __assertMasterPasswordAndKeyValid(self):
        """Asserts that the master password and key matches the one present in database.
        Master password and key is stored as SHA2 in a single row in the master collection.
        """
        cursor = self.master_password_collection.find()
        assert cursor.count() == 1, ERROR_MULTIPLE_MASTER_ROWS
        document = cursor.next()
        assert document[MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD] == generate_hash(
            self.request.form.get(BODY_MASTER_PASSWORD_PARAM)), ERROR_MASTER_PASSWORD
        assert document[MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD] == generate_hash(
            self.request.form.get(BODY_MASTER_KEY_PARAM)), ERROR_MASTER_KEY
