from crypto.encrypter import Encrypter
from crypto.decrypter import Decrypter
from utils.test import create_random_string, create_random_master_key

MAX_STRING_LENGTH = 16
MAX_MASTER_KEY_VALUE = 10000
TEST_ITERATION_COUNT = 100


def test_encryption_decryption():
    """This test runs TEST_ITERATION_COUNT times. 
    A random string is generated with a random master password and key.
    The random string is encrypted and decryted back and assertion is made that the decrypted string is the original string.
    """
    for _ in range(TEST_ITERATION_COUNT):
        master_password = create_random_string(MAX_STRING_LENGTH)
        master_key = create_random_master_key(MAX_MASTER_KEY_VALUE)
        test_string = create_random_string(MAX_STRING_LENGTH)
        encrypter = Encrypter(master_password, master_key)
        decrypter = Decrypter(master_password, master_key)
        encrypted_string = encrypter.encrypt(test_string)
        decrypted_string = decrypter.decrypt(encrypted_string)
        assert test_string, decrypted_string
