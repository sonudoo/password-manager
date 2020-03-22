# Mongo DB connection uri. It must be specified without database.
MONGO_URI = ""

# Name of the database. The database must contain three collections as defined below.
DATABASE_NAME = 'pwdmngr'

# The collection in which all the secrets are stored.
PASSWORD_MANAGER_COLLECTION_NAME = 'pwdmngr'
# The collection in which auth keys are stored.
AUTH_COLLECTION_NAME = 'auth'
# The collection in which master password and master key is stored in a single row.
MASTER_PASSWORD_COLLECTION_NAME = 'master'

# Password manager collection fields
PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD = 'domain'
PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD = 'username'
PASSWORD_MANAGER_COLLECTION_SECRETS_FIELD = 'secrets'

# Auth collection fields
AUTH_COLLECTION_KEY_FIELD = 'key'

# Master collection fields
MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD = 'master-password'
MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD = 'master-key'
