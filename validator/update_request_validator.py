from constants.request_parameters import BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM, BODY_NEW_USERNAME_PARAM, BODY_NEW_SECRET_PARAM
from constants.database import PASSWORD_MANAGER_COLLECTION_NAME, PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD, PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD
from constants.response_messages import ERROR_DOMAIN_REQUIRED, ERROR_USERNAME_SPECIFIED_BUT_BLANK, ERROR_NEW_USERNAME_SPECIFIED_BUT_BLANK, ERROR_NEW_SECRET_SPECIFIED_BUT_BLANK, ERROR_SINGLE_RECORD_MATCH_REQUIRED_FOR_UPDATE, ERROR_DUPLICATE_DOMAIN_NEW_USERNAME, ERROR_OLD_AND_NEW_USERNAME_SAME
import hashlib
from validator.request_validator import RequestValidator


class UpdateRequestValidator(RequestValidator):
    """Child class for validation of update requests.

    isValid() of this class calls isValid() of parent class.

    Attributes:
        password_manager_collection (Collection): Password manager collection.
    """
    password_manager_collection = None

    def __init__(self, request, dbclient):
        """
        Args:
            request (Request): The flask request received from the client.
            dbclient (DbClient): The database client object.
        """
        super().__init__(request, dbclient)
        self.password_manager_collection = dbclient.get_collection(
            PASSWORD_MANAGER_COLLECTION_NAME)

    def isValid(self):
        """ Validates the update requests. Calls into parent's isValid() function.
        The following validations are performed:

        1. Domain exists and is non-empty.
        2. If username exists, then it is non-empty.
        3. If new username exists, then it is non-empty.
        4. All new secrets are valid and non-empty.
        5. The domain (and username if specified) combination matches exactly one record in the password manager collection.
           If the new username is specified, then the existing username must not be same as the new username.
        6. If new username exists, the domain and new username combination is unique in the password manager collection.
        Returns:
            ((bool, str)): Whether the update request is valid or not, Error message if any.
        """
        try:
            super().isValid()
            self.__assertDomainFieldExistsInRequest()
            self.__assertIfUsernameExistsThenIsValid()
            self.__assertIfNewUsernameExistsThenIsValid()
            self.__assertIfNewSecretExistsThenIsValid()
            self.__assertOneRecordForDomainAndUsername()
            self.__assertIfNewUsernameThenDomainAndNewUsernameUnique()
            return True, None
        except Exception as e:
            message = e.args[0]
            return False, message

    def __assertDomainFieldExistsInRequest(self):
        """Asserts that the domain field exists and is non-empty."""
        assert self.request.form.get(
            BODY_DOMAIN_PARAM) != None, ERROR_DOMAIN_REQUIRED
        assert len(self.request.form.get(BODY_DOMAIN_PARAM)
                   ) > 0, ERROR_DOMAIN_REQUIRED

    def __assertIfUsernameExistsThenIsValid(self):
        """Asserts that if the username field exists then it is non-empty."""
        if self.request.form.get(BODY_USERNAME_PARAM) != None:
            assert len(self.request.form.get(BODY_USERNAME_PARAM)
                       ) > 0, ERROR_USERNAME_SPECIFIED_BUT_BLANK

    def __assertIfNewUsernameExistsThenIsValid(self):
        """Asserts that if the new username field exists then it is non-empty."""
        if self.request.form.get(BODY_NEW_USERNAME_PARAM) != None:
            assert len(self.request.form.get(BODY_NEW_USERNAME_PARAM)
                       ) > 0, ERROR_NEW_USERNAME_SPECIFIED_BUT_BLANK

    def __assertIfNewSecretExistsThenIsValid(self):
        """Asserts that if the new secrets field exists then all secrets are valid."""
        if self.request.form.getlist(BODY_NEW_SECRET_PARAM) != None:
            secrets = self.request.form.getlist(BODY_NEW_SECRET_PARAM)
            for secret in secrets:
                assert secret != None, ERROR_NEW_SECRET_SPECIFIED_BUT_BLANK
                assert len(secret) > 0, ERROR_NEW_SECRET_SPECIFIED_BUT_BLANK

    def __assertOneRecordForDomainAndUsername(self):
        """Asserts that the domain (and username if exists) matches exatly one record in the password manager collection.
        Also asserts that the new username is not same as the old username in the record."""
        cursor = None
        if self.request.form.get(BODY_USERNAME_PARAM) == None:
            cursor = self.password_manager_collection.find({
                PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: self.request.form.get(BODY_DOMAIN_PARAM),
            })
        else:
            cursor = self.password_manager_collection.find({
                PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: self.request.form.get(BODY_DOMAIN_PARAM),
                PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: self.request.form.get(
                    BODY_USERNAME_PARAM)
            })
        assert cursor.count() == 1, ERROR_SINGLE_RECORD_MATCH_REQUIRED_FOR_UPDATE
        if self.request.form.get(BODY_NEW_USERNAME_PARAM) != None:
            assert cursor.next()[PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD] != self.request.form.get(
                BODY_NEW_USERNAME_PARAM), ERROR_OLD_AND_NEW_USERNAME_SAME

    def __assertIfNewUsernameThenDomainAndNewUsernameUnique(self):
        """Asserts that if the new username field exists, then the domain and new username combination is non-empty."""
        if self.request.form.get(BODY_NEW_USERNAME_PARAM) != None:
            cursor = self.password_manager_collection.find({
                PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: self.request.form.get(BODY_DOMAIN_PARAM),
                PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: self.request.form.get(
                    BODY_NEW_USERNAME_PARAM)
            })
            assert cursor.count() == 0, ERROR_DUPLICATE_DOMAIN_NEW_USERNAME
