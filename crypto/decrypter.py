import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from crypto.cipher_key import CipherKey


class Decrypter:
    """A wrapper class for decryption

    This class uses AES cipher to decrypt strings. Cipher Block Chain mode is used for AES.

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

    def decrypt(self, encrypted_base64_string):
        """Decrypts an encrypted base64 string using AESCipher and returns a utf-8 string of the decrypted bytes.
        Decryption works as follows:
        1. The ASCII base64 string is encoded to bytes.
        2. The base64 bytes are converted to normal bytes (Every 8 bits are converted to 6 bit)
        3. The bytes are decrypted.
        4. The decrypted bytes are unpadded using AES block size.
        5. The bytes are then decoded to utf-8 string.

        Args:
            string (str): The base64 encrypted string to be encrypted.

        Returns:
            string: Decrypted bytes as utf-8 string
        """
        encrypted_base64_bytes = encrypted_base64_string.encode('ascii')
        encrypted_bytes = base64.b64decode(encrypted_base64_bytes)
        padded_encoded_bytes = self.cipher.decrypt(encrypted_bytes)
        encoded_bytes = unpad(padded_encoded_bytes, AES.block_size)
        return encoded_bytes.decode('utf-8')
