from constants.database import AUTH_COLLECTION_NAME, AUTH_COLLECTION_KEY_FIELD
from utils.hash import generate_hash


class Authenticator:
    """A wrapper class for authentication

    Attributes:
        auth_collection (Collection): The collection where auth keys are stored in each row.
    """
    auth_collection = None

    def __init__(self, dbclient):
        """
        Args:
            dbclient (DbClient): The database client object.
        """
        self.auth_collection = dbclient.get_collection(AUTH_COLLECTION_NAME)

    def authenticate(self, key):
        """ Authenticates a key.
        Args:
            key (str): The authentication key whose hash is present in the auth collection.
        Returns:
            bool: True of the hash of the auth key was found, False otherwise.
        """
        cursor = self.auth_collection.find({
            AUTH_COLLECTION_KEY_FIELD: generate_hash(key)
        })
        return cursor != None and cursor.count() != 0
