from constants.request_parameters import BODY_DOMAIN_PARAM, BODY_USERNAME_PARAM, BODY_QUERY_TYPE_PARAM, BODY_SECRET_PARAM, BODY_MASTER_PASSWORD_PARAM, BODY_MASTER_KEY_PARAM, BODY_NEW_USERNAME_PARAM, BODY_NEW_SECRET_PARAM
from constants.database import MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD, MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD, PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD, PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD, AUTH_COLLECTION_KEY_FIELD
from crypto.cipher_key import CipherKey
from mock import Mock
import random
import string
from utils.hash import generate_hash


def create_cipher_key(master_password, master_key):
    """Creates an instance of CipherKey using the master password and key
    Args:
        master_password (str): Master password for the cipher key
        master_key (str): Master key for the cipher key
    Returns:
        CipherKey: Instance of CipherKey
    """
    cipher_key_builder = CipherKey.Builder()
    cipher_key_builder.set_master_password(master_password)
    cipher_key_builder.set_master_key(master_key)
    cipher_key = cipher_key_builder.build()
    return cipher_key


def create_random_string(max_length):
    """Creates a random non-empty string of given maximum length.
    Args:
        max_length (int): Maximum length of the string to be generated.
    Returns:
        str: Generated non-empty random string
    """
    length = random.randint(1, max_length)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def create_random_master_key(max_value):
    """Creates a random master key of given maximum value.
    Args:
        max_value (int): Maximum value of master key.
    Returns:
        int: Generated non-negative random key
    """
    return random.randint(0, max_value)


def create_mock_request(domain=None, username=None, query_type=None, secret=None, master_password=None, master_key=None, new_username=None, new_secret=None):
    """Creates a mock flask Request object that returns the provided value when get() or getlist() is called on form attribute.
    Defaults to returning None.
    Args:
        domain (str, optional): The domain body parameter in the request.
        username (str, optional): The username body parameter in the request.
        query_type (str, optional): The query-type body parameter in the request.
        secret (list, optional): The secret body parameter in the request.
        master_password (str, optional): The master-password body parameter in the request.
        master_key (str, optional): The master key body parameter in the request.
        new-username (str, optional): The new-username body parameter in the request.
        new-secret (list, optional): The new-secret body parameter in the request.
    Returns:
        Mock: Mock Request object.
    """
    def request_form_get(param):
        """This method stubs the request.form.get() method."""
        if param == BODY_DOMAIN_PARAM:
            return domain
        elif param == BODY_USERNAME_PARAM:
            return username
        elif param == BODY_NEW_USERNAME_PARAM:
            return new_username
        elif param == BODY_QUERY_TYPE_PARAM:
            return query_type
        elif param == BODY_MASTER_PASSWORD_PARAM:
            return master_password
        elif param == BODY_MASTER_KEY_PARAM:
            return master_key
        else:
            return None

    def request_form_getlist(param):
        """This method stubs the request.form.getlist() method."""
        if param == BODY_SECRET_PARAM:
            return secret
        elif param == BODY_NEW_SECRET_PARAM:
            return new_secret
        else:
            return None

    request = Mock()
    request.form.get = Mock(side_effect=request_form_get)
    request.form.getlist = Mock(side_effect=request_form_getlist)
    return request


def create_mock_dbclient(collection=None):
    """Creates a mock DbClient that returns the given collection when get_collection() is called.
    Defaults to returning None.
    Args:
        collection (Collection|Mock, optional): A collection to return which can itself be a mock.
    Returns:
        Mock: Mock DbClient object.
    """
    def get_collection(param):
        """This method stubs get_collection() method."""
        return collection

    dbclient = Mock()
    dbclient.get_collection = Mock(side_effect=get_collection)
    return dbclient


def create_mock_collection(find_return_value1=None, find_return_value2=None, find_return_value3=None):
    """Creates a mock Collection that returns the given cursors when find()/find_one() is called.
    Defaults to returning None.
    Args:
        find_return_value1 (Cursor|Mock, optional): A cursor/mock to return when find()/find_one() is called for the first time.
        find_return_value2 (Cursor|Mock, optional): A cursor/mock to return when find()/find_one() is called for the second time.
        find_return_value3 (Cursor|Mock, optional): A cursor/mock to return when find()/find_one() is called for the third time.
    Returns:
        Mock: Mock Collection object.
    """
    def find1(param=None):
        return find_return_value1

    def find2(param=None):
        return find_return_value2

    def find3(param=None):
        return find_return_value3

    collection = Mock()
    collection.find = Mock(side_effect=[find1(), find2(), find3()])
    collection.find_one = Mock(side_effect=[find1(), find2(), find3()])
    return collection


def create_mock_cursor(cursor_values=[]):
    """Creates a mock Cursor that returns the given cursor values when iterated.
    Defaults to an empty cursor.
    Args:
        cursor_values (list, optional): A list of objects that the cursor holds.
    Returns:
        Mock: Mock Collection object.
    """
    class MockCursor:
        """Mock class for the cursor objects.

        Attributes:
            current_index (int): Current index that the cursor pointer is pointing to.
            cursor_values(list): A list of objects that the cursor holds.
        """
        current_index = None
        cursor_values = None

        def __init__(self, cursor_values=[]):
            self.current_index = 0
            self.cursor_values = cursor_values

        def count(self):
            """This methods mocks the count() method of cursor."""
            return len(self.cursor_values)

        def next(self):
            """This methods mocks the next() method of cursor."""
            if self.current_index >= len(self.cursor_values):
                return None
            else:
                self.current_index += 1
                return self.cursor_values[self.current_index - 1]

    cursor = MockCursor(cursor_values)
    return cursor


def create_mock_dbclient_with_master_collection(master_password, master_key):
    """Creates a mock DbClient with a mock master collection that is returned as a return of get_collection.
    Args:
        master_password (str): Master password whose hash is stored in the master collection mock.
        master_key (str): Master key whose hash is stored in the master collection mock.
    Returns:
        Mock: Mock DbClient object.
    """
    master_collection = create_mock_cursor(cursor_values=[{
        MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD: generate_hash(master_password),
        MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD: generate_hash(master_key)
    }])
    return create_mock_dbclient(collection=create_mock_collection(find_return_value1=master_collection))


def create_mock_dbclient_with_master_and_password_manager_collection(master_password, master_key, domain, username):
    """Creates a mock DbClient with a mock master collection and mock password manager collection.
    The master collection is returned as a result of first find()/find_one().
    The password manager collection is returned as a result of second find()/find_one().
    Args:
        master_password (str): Master password whose hash is stored in the master collection mock.
        master_key (str): Master key whose hash is stored in the master collection mock.
    Returns:
        Mock: Mock DbClient object.
    """
    master_collection = create_mock_cursor(cursor_values=[{
        MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD: generate_hash(master_password),
        MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD: generate_hash(master_key)
    }])
    password_manager_collection = None
    if domain and username:
        password_manager_collection = create_mock_cursor(cursor_values=[{
            PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: domain,
            PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: username
        }])
    else:
        password_manager_collection = create_mock_cursor()
    return create_mock_dbclient(collection=create_mock_collection(find_return_value1=master_collection, find_return_value2=password_manager_collection))


def create_mock_dbclient_with_master_and_multiple_password_manager_collection(master_password, master_key, domain1, username1, domain2, username2):
    """Creates a mock DbClient with a mock master collection and two mock password manager collection.
    The master collection is returned as a result of first find()/find_one().
    The 1st password manager collection is returned as a result of second find()/find_one().
    The 2nd password manager collection is returned as a result of third find()/find_one().
    Args:
        master_password (str): Master password whose hash is stored in the master collection mock.
        master_key (str): Master key whose hash is stored in the master collection mock.
        domain1 (str): Domain for a record returned by 1st password manager collection mock.
        username1 (str): Username for the same record returned by 1st password manager collection mock.
        domain2 (str): Domain for a record returned by 2nd password manager collection mock.
        username2 (str): Username for the same record returned by 2nd password manager collection mock.
    Returns:
        Mock: Mock DbClient object.
    """
    master_collection = create_mock_cursor(cursor_values=[{
        MASTER_PASSWORD_COLLECTION_MASTER_PASSWORD_FIELD: generate_hash(master_password),
        MASTER_PASSWORD_COLLECTION_MASTER_KEY_FIELD: generate_hash(master_key)
    }])
    password_manager_collection1 = None
    if domain1 and username1:
        password_manager_collection1 = create_mock_cursor(cursor_values=[{
            PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: domain1,
            PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: username1
        }])
    else:
        password_manager_collection1 = create_mock_cursor()
    password_manager_collection2 = None
    if domain2 and username2:
        password_manager_collection2 = create_mock_cursor(cursor_values=[{
            PASSWORD_MANAGER_COLLECTION_DOMAIN_FIELD: domain2,
            PASSWORD_MANAGER_COLLECTION_USERNAME_FIELD: username2
        }])
    else:
        password_manager_collection2 = create_mock_cursor()
    return create_mock_dbclient(collection=create_mock_collection(find_return_value1=master_collection, find_return_value2=password_manager_collection1, find_return_value3=password_manager_collection2))


def create_mock_dbclient_with_auth_collection(key):
    """Creates a mock DbClient with a mock auth collection.
    The auth collection is returned as a result of find()/find_one().
    Args:
        key (str): The key which is hashed as stored in auth collection.
    Returns:
        Mock: Mock DbClient object.
    """
    auth_collection = None
    if key != None:
        auth_collection = create_mock_cursor(cursor_values=[{
            AUTH_COLLECTION_KEY_FIELD: generate_hash(key)
        }])
    else:
        auth_collection = create_mock_cursor()
    return create_mock_dbclient(collection=create_mock_collection(find_return_value1=auth_collection))
