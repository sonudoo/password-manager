from constants.database import PASSWORD_MANAGER_COLLECTION_NAME, PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD, PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD, PASSWORD_MANAGER_COLLECTION_SECRETS_FIELD
from constants.request_parameters import BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM, BODY_SECRET_PARAM, BODY_MASTER_PASSWORD_PARAM, BODY_MASTER_KEY_PARAM
from crypto.encrypter import Encrypter


class InsertProcessor:
    """A wrapper class for processing insert requests

    Attributes:
        collection (Collection): The password manager collection object.
        domain (str): The domain for the record.
        username (str): The username for the record.
        secrets (list): The secrets for the record.
        encrypter (Encrypter): The Encrypter object to encrypt all the secrets.
    """
    collection = None
    domain = None
    username = None
    secrets = None
    encrypter = None

    def __init__(self, request, dbclient):
        """
        Args:
            request (Request): The flask request object received from the client.
            dbclient (DbClient): The database client object.
        """
        self.collection = dbclient.get_collection(
            PASSWORD_MANAGER_COLLECTION_NAME)
        master_password = request.form.get(BODY_MASTER_PASSWORD_PARAM)
        master_key = int(request.form.get(BODY_MASTER_KEY_PARAM))
        self.domain = request.form.get(BODY_DOMAIN_PARAM)
        self.username = request.form.get(BODY_USERNAME_PARAM)
        self.secrets = request.form.getlist(BODY_SECRET_PARAM)
        self.encrypter = Encrypter(master_password, master_key)

    def process(self):
        """Inserts the record to the password manager collection."""
        encrypted_secrets = self.__encrypt_secrets(self.secrets)
        self.collection.insert_one({
            PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: self.domain,
            PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: self.username,
            PASSWORD_MANAGER_COLLECTION_SECRETS_FIELD: encrypted_secrets
        })

    def __encrypt_secrets(self, secrets):
        """Encrypts all the secrets in a list.
        Args:
            secrets (list): List of secrets to encrypt.
        Returns:
            list: List of corresponding encrypted secrets.
        """
        return [self.encrypter.encrypt(secret) for secret in secrets]
