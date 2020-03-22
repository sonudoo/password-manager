from constants.database import PASSWORD_MANAGER_COLLECTION_NAME, PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD, PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD, PASSWORD_MANAGER_COLLECTION_SECRETS_FIELD
from constants.request_parameters import BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM, BODY_SECRET_PARAM, BODY_MASTER_PASSWORD_PARAM, BODY_QUERY_TYPE_PARAM, BODY_MASTER_KEY_PARAM, QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE, QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE
from constants.response_messages import ERROR_MULTIPLE_RECORDS_FOUND_FOR_DECRYPTING_SECRETS, ERROR_NO_RECORD_FOUND
from crypto.decrypter import Decrypter


class QueryProcessor:
    """A wrapper class for processing query requests

    Attributes:
        collection (Collection): The password manager collection object.
        domain (str): The domain for the record.
        username (str): The username for the record.
        decrypter (Decrypter): The Decrypter object to decrypt the secrets. Only initialized if query type is QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE.
        query_type (str): The type of query.
    """
    collection = None
    domain = None
    username = None
    decrypter = None
    query_type = None

    def __init__(self, request, dbclient):
        """
        Args:
            request (Request): The flask request object received from the client.
            dbclient (DbClient): The database client object.
        """
        self.collection = dbclient.get_collection(
            PASSWORD_MANAGER_COLLECTION_NAME)
        self.query_type = request.form.get(BODY_QUERY_TYPE_PARAM)
        if self.query_type == QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE:
            master_password = request.form.get(BODY_MASTER_PASSWORD_PARAM)
            master_key = int(request.form.get(BODY_MASTER_KEY_PARAM))
            self.decrypter = Decrypter(master_password, master_key)

        self.domain = request.form.get(BODY_DOMAIN_PARAM)
        self.username = request.form.get(BODY_USERNAME_PARAM)

    def process(self):
        """Queries the password manager collection.
        If query type is QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE, it filters the records by domain (and username).
        If query type is QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE, it decrypts the secrets and returns them if and only if a single record is found for requested domain (and username).
        """
        if self.query_type == QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE:
            cursor = self.collection.find()
            return self.__filter_by_domain_and_username(cursor)
        elif self.query_type == QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE:
            cursor = None
            if self.username == None:
                cursor = self.collection.find({
                    PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: self.domain
                })
            else:
                cursor = self.collection.find({
                    PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: self.domain,
                    PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: self.username
                })
            if cursor.count() > 1:
                raise Exception(
                    ERROR_MULTIPLE_RECORDS_FOUND_FOR_DECRYPTING_SECRETS)
            elif cursor.count() == 0:
                raise Exception(ERROR_NO_RECORD_FOUND)
            else:
                record = cursor.next()
                return {
                    PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: record[PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD],
                    PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: record[PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD],
                    PASSWORD_MANAGER_COLLECTION_SECRETS_FIELD: self.__decrypt_secrets(
                        record[PASSWORD_MANAGER_COLLECTION_SECRETS_FIELD])
                }

    def __filter_by_domain_and_username(self, cursor):
        """Filters the cursor by domain (and username if specified in request).
        For a match, the lowercase of paramater in request must be a substring of the corresponding field in collection.
        Args:
            cursor (Cursor): The cursor object which is a result of find()/find_one() on a collection object.
        Returns:
            list: A list of filtered objects having domain and username.
        """
        result = []
        for _ in range(cursor.count()):
            record = cursor.next()
            domain = record[PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD]
            username = record[PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD]
            if self.domain.lower() in domain.lower():
                if self.username != None:
                    if self.username.lower() in username.lower():
                        result.append({
                            PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: domain,
                            PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: username
                        })
                else:
                    result.append({
                        PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: domain,
                        PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: username
                    })
        return result

    def __decrypt_secrets(self, secrets):
        """Decrypts all the secrets in a list.
        Args:
            secrets (list): List of encrypted secrets to decrypt.
        Returns:
            list: List of corresponding decrypted secrets.
        """
        assert self.decrypter != None
        return [self.decrypter.decrypt(secret) for secret in secrets]
