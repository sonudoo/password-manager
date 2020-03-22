# Header parameter that the user can use to specify the authentication key.
HEADERS_AUTH_KEY_PARAM = 'auth-key'

# Body parameter that the user can use to specify the master password for all operations.
BODY_MASTER_PASSWORD_PARAM = 'master-password'
# Body parameter that the user can use to specify the master key for all operations.
BODY_MASTER_KEY_PARAM = 'master-key'
# Body parameter that the user can use to specify the domain for all operations.
BODY_DOMAIN_PARAM = 'domain'
# Body parameter that the user can use to specify the username for all operations.
BODY_USERNAME_PARAM = 'username'
# Body parameter that the user can use to specify a list of secrets for insert operation.
BODY_SECRET_PARAM = 'secret'

# Body parameter that the user can use to specify the query type for query requests.
BODY_QUERY_TYPE_PARAM = 'query-type'

# Body parameter value for first query type. This is used for searching the password manager collection by given domain and username.
QUERY_SEARCH_BY_DOMAIN_AND_USERNAME_TYPE = '1'
# Body parameter value for second query type. This is used for decrypting all secrets of single record match.
QUERY_GET_SECRETS_FOR_DOMAIN_AND_USERNAME_TYPE = '2'

# Body parameter that the user can use to specify the new username for update operation.
BODY_NEW_USERNAME_PARAM = 'new-username'
# Body parameter that the user can use to specify a list of new secrets for update operation.
BODY_NEW_SECRET_PARAM = 'new-secret'
