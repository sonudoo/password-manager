from constants.request_parameters import BODY_QUERY_TYPE_PARAM, BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM, BODY_SECRET_PARAM, QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE, QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE
from constants.response_messages import ERROR_DOMAIN_REQUIRED, ERROR_USERNAME_REQUIRED, ERROR_SECRETS_REQUIRED, ERROR_ATLEAST_ONE_SECRET_REQUIRED, ERROR_DUPLICATE_DOMAIN_USERNAME, ERROR_QUERY_TYPE_REQUIRED, ERROR_USERNAME_SPECIFIED_BUT_BLANK
from validator.request_validator import RequestValidator


class QueryRequestValidator(RequestValidator):
    """Child class for validation of query requests.

    isValid() of this class calls isValid() of parent class.

    Attributes:
        password_manager_collection (Collection): Password manager collection.
        acceptable_query_type (list): A list of query type that are valid.
    """
    password_manager_collection = None
    acceptable_query_type = None

    def __init__(self, request, dbclient, acceptable_query_type=[QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE, QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE]):
        """
        Args:
            request (Request): The flask request received from the client.
            dbclient (DbClient): The database client object.
            acceptable_query_type (list, optional): By default, QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE and QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE are acceptable.
        """
        super().__init__(request, dbclient)
        self.acceptable_query_type = acceptable_query_type

    def isValid(self):
        """ Validates the query requests. Calls into parent's isValid() function.
        The following validations are performed:

        1. Query type parameter exists and the query type is acceptable.
        2. Domain exists and is non-empty.
        3. If the username exists in request, then it should be non-empty.
        Returns:
            ((bool, str)): Whether the query request is valid or not, Error message if any.
        """
        try:
            super().isValid()
            self.__assertQueryTypeFieldExistsInRequest()
            self.__assertQueryTypeIsAcceptable()
            self.__assertDomainFieldExistsInRequest()
            self.__assertIfUsernameExistsThenIsValid()
            return True, None
        except Exception as e:
            message = e.args[0]
            return False, message

    def __assertQueryTypeFieldExistsInRequest(self):
        """Asserts that the query type parameters exists in the request."""
        assert self.request.form.get(
            BODY_QUERY_TYPE_PARAM) != None, ERROR_QUERY_TYPE_REQUIRED

    def __assertQueryTypeIsAcceptable(self):
        """Asserts that the query type parameters is acceptable."""
        assert self.request.form.get(
            BODY_QUERY_TYPE_PARAM) in self.acceptable_query_type, ERROR_QUERY_TYPE_REQUIRED

    def __assertDomainFieldExistsInRequest(self):
        """Asserts that the domain parameters exists in the request and it is non-empty."""
        assert self.request.form.get(
            BODY_DOMAIN_PARAM) != None, ERROR_DOMAIN_REQUIRED
        assert len(self.request.form.get(BODY_DOMAIN_PARAM)
                   ) > 0, ERROR_DOMAIN_REQUIRED

    def __assertIfUsernameExistsThenIsValid(self):
        """Asserts that if the username parameters exists in the request it is non-empty."""
        if self.request.form.get(BODY_USERNAME_PARAM) != None:
            assert len(self.request.form.get(BODY_USERNAME_PARAM)
                       ) > 0, ERROR_USERNAME_SPECIFIED_BUT_BLANK
