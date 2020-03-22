from constants.database import PASSWORD_MANAGER_COLLECTION_NAME, PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD, PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD, PASSWORD_MANAGER_COLLECTION_SECRETS_FIELD
from constants.request_parameters import BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM, BODY_NEW_USERNAME_PARAM, BODY_NEW_SECRET_PARAM, BODY_MASTER_PASSWORD_PARAM, BODY_MASTER_KEY_PARAM
from crypto.encrypter import Encrypter


class UpdateProcessor:
    """A wrapper class for processing update requests

    Attributes:
        collection (Collection): The password manager collection object.
        domain (str): The domain for the record.
        username (str): The username for the record.
        new_username (str): New username for the record.
        new_secrets (list): New secrets for the record.
        encrypter (Encrypter): The Encrypter object to encrypt the secrets. It is initialized only if atleast one new secret is specified.
    """
    collection = None
    domain = None
    username = None
    new_username = None
    new_secrets = None
    encrypter = None

    def __init__(self, request, dbclient):
        """
        Args:
            request (Request): The flask request object received from the client.
            dbclient (DbClient): The database client object.
        """
        self.collection = dbclient.get_collection(
            PASSWORD_MANAGER_COLLECTION_NAME)
        self.domain = request.form.get(BODY_DOMAIN_PARAM)
        self.username = request.form.get(BODY_USERNAME_PARAM)
        self.new_username = request.form.get(BODY_NEW_USERNAME_PARAM)
        self.new_secrets = request.form.getlist(BODY_NEW_SECRET_PARAM)
        if self.new_secrets != None:
            master_password = request.form.get(BODY_MASTER_PASSWORD_PARAM)
            master_key = int(request.form.get(BODY_MASTER_KEY_PARAM))
            self.encrypter = Encrypter(master_password, master_key)

    def process(self):
        """Updates a single record.
        If new username is specified then the existing username is replaced.
        If new secrets are specified, then the existing secrets are replaced."""
        query = {PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: self.domain}
        if self.username != None:
            query[PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD] = self.username
        new_values = {}
        if self.new_username != None:
            new_values[PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD] = self.new_username
        if self.new_secrets != None and len(self.new_secrets) > 0:
            new_values[PASSWORD_MANAGER_COLLECTION_SECRETS_FIELD] = self.__encrypt_secrets(
                self.new_secrets)
        self.collection.update_one(query, {'$set': new_values})

    def __encrypt_secrets(self, secrets):
        """Encrypts all the secrets in a list.
        Args:
            secrets (list): List of secrets to encrypt.
        Returns:
            list: List of corresponding encrypted secrets.
        """
        assert self.encrypter != None
        return [self.encrypter.encrypt(secret) for secret in secrets]
