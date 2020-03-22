from constants.request_parameters import BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM, BODY_SECRET_PARAM
from constants.database import PASSWORD_MANAGER_COLLECTION_NAME, PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD, PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD
from constants.response_messages import ERROR_DOMAIN_REQUIRED, ERROR_USERNAME_REQUIRED, ERROR_SECRETS_REQUIRED, ERROR_ATLEAST_ONE_SECRET_REQUIRED, ERROR_DUPLICATE_DOMAIN_USERNAME
from validator.request_validator import RequestValidator


class InsertRequestValidator(RequestValidator):
    """Child class for validation of insert requests.

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
        """ Validates the insert requests. Calls into parent's isValid() function.
        The following validations are performed:

        1. Domain exists and is non-empty.
        2. Username exists and is non-empty.
        3. At one secret exists in the request list.
        4. All secrets are non-empty.
        5. The domain and username combination is unique and doesn't already exist in the password manager collection.
        Returns:
            ((bool, str)): Whether the insert request is valid or not, Error message if any.
        """
        try:
            super().isValid()
            self.__assertDomainFieldExistsInRequest()
            self.__assertUsernameFieldExistsInRequest()
            self.__assertAtleastOneSecretFieldExistsInRequest()
            self.__assertAllSecretsAreValid()
            self.__assertUniqueDomainAndUsername()
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

    def __assertUsernameFieldExistsInRequest(self):
        """Asserts that the username field exists and is non-empty."""
        assert self.request.form.get(
            BODY_USERNAME_PARAM) != None, ERROR_USERNAME_REQUIRED
        assert len(self.request.form.get(BODY_USERNAME_PARAM)
                   ) > 0, ERROR_USERNAME_REQUIRED

    def __assertAtleastOneSecretFieldExistsInRequest(self):
        """Asserts that at least one secret field exists in the request."""
        assert self.request.form.getlist(
            BODY_SECRET_PARAM) != None, ERROR_ATLEAST_ONE_SECRET_REQUIRED
        assert len(self.request.form.getlist(BODY_SECRET_PARAM)
                   ) > 0, ERROR_ATLEAST_ONE_SECRET_REQUIRED

    def __assertAllSecretsAreValid(self):
        """Asserts that all secrets are valid and non-empty."""
        secrets = self.request.form.getlist(BODY_SECRET_PARAM)
        for secret in secrets:
            assert secret != None, ERROR_SECRETS_REQUIRED
            assert len(secret) > 0, ERROR_SECRETS_REQUIRED

    def __assertUniqueDomainAndUsername(self):
        """Asserts that the domain and username combination is unique."""
        cursor = self.password_manager_collection.find({
            PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: self.request.form.get(BODY_DOMAIN_PARAM),
            PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: self.request.form.get(
                BODY_USERNAME_PARAM)
        })
        assert cursor.count() == 0, ERROR_DUPLICATE_DOMAIN_USERNAME
