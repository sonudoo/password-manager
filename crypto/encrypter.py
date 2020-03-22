import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from crypto.cipher_key import CipherKey


class Encrypter:
    """A wrapper class for encryption

    This class uses AES cipher to encrypt strings. Cipher Block Chain mode is used for AES.

    Attributes:
        cipher (AESCipher): The AES cipher
    """
    cipher = None

    def __init__(self, master_password, master_key):
        """
        A new CipherKey object is created using the given master password and master key.
        The key binary of CipherKey is then used as key and initialization vector for AES cipher.
        Args:
            master_password (str): Master password for key generation.
            master_key (int): Master key for key generation.
        """
        cipher_key_builder = CipherKey.Builder()
        cipher_key_builder.set_master_password(master_password)
        cipher_key_builder.set_master_key(master_key)
        cipher_key = cipher_key_builder.build().get_binary()
        self.cipher = AES.new(cipher_key, AES.MODE_CBC, cipher_key)

    def encrypt(self, string):
        """Encrypts the string using AESCipher and returns a base64 string of the encrypted bytes.
        Encryption works as follows:
        1. Encode the string to bytes.
        2. Pad the bytes to the block size of AES.
        3. Encrypt the bytes.
        4. The encrypted bytes are converted to base 64 bytes (Every 6 bits are converted to 8 bit that corresponds to a ASCII character).
        5. The base 64 bytes are decoded as an ASCII string.

        Args:
            string (str): The string to be encrypted.

        Returns:
            string: Encrypted bytes as base64 string
        """
        encoded_bytes = string.encode('utf-8')
        padded_encoded_bytes = pad(encoded_bytes, AES.block_size)
        encrypted_bytes = self.cipher.encrypt(padded_encoded_bytes)
        encrypted_base64_bytes = base64.b64encode(encrypted_bytes)
        return encrypted_base64_bytes.decode('ascii')
