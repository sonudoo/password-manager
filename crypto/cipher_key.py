import random
from constants.key_config import CIPHER_KEY_MOD, CIPHER_KEY_LENGTH, CIPHER_KEY_CHURN_COUNT, CIPHER_KEY_ASCII_LIM


class CipherKey:
    """Stores the key which is used for encrypting and decrypting all the secrets.

    The key is generated from master password and master key using a generation algorithm.

    Attributes:
        master_password (str): Master password passed by client.
        master_key (int): Master key passed by client.
        key (str): The generated key.
    """
    master_password = None
    master_key = None
    key = None

    def __init__(self, master_password, master_key):
        """
        Args:
            master_password (str): Master password for key generation.
            master_key (int): Master key for key generation.
        """
        self.master_password = master_password
        self.master_key = master_key
        self.__generate_key()

    def get_string(self):
        """
        Returns:
            string: Cipher key as utf-8 string
        """
        return self.key

    def get_binary(self):
        """
        Returns:
            bytes: Cipher key as bytes
        """
        return self.key.encode('utf-8')

    def __generate_key(self):
        """
        The following algorithm is used for key generation:

        1. The delta for caesar cipher is computed as the mod inverse of master key under self.MOD.
        2. The randomizer is seeded with the master key.
        3. The key is initialized to the master password.
        3. The key is trimmed (if length is greater than CIHER_KEY_LENGTH) or padded (by repeatation, if length is less than CIHER_KEY_LENGTH).
        4. For CIPHER_KEY_CHURN_COUNT number of times,
            a. Caesar cipher is applied to the key.
            b. The key is then randomized.
            c. The delta for caesar cipher is re-computed as the mod inverse of existing delta under self.MOD.
        """
        if self.master_password == None or self.master_password == '':
            raise Exception('Master Key should be at least one character long')
        if self.master_key == None or self.master_key < 0:
            raise Exception('Master Password must be a non-negative integer')

        caesar_delta = self.__mod_inverse(self.master_key)
        random.seed(self.master_key)
        self.key = self.master_password
        self.__trim()
        self.__pad()
        for _ in range(CIPHER_KEY_CHURN_COUNT):
            self.__apply_caesar(caesar_delta)
            self.__randomize()
            caesar_delta = self.__mod_inverse(caesar_delta)

    def __mod_inverse(self, number):
        """Computes the modular inverse of the number under CIPHER_KEY_MOD.
        Args:
            number (int): The number whose modular inverse is to be calculated.

        Returns:
            int: Modular inverse of number under CIPHER_KEY_MOD.
        """
        result = 1
        power = CIPHER_KEY_MOD - 2
        while power > 0:
            if (power & 1) > 0:
                result *= number
                result %= CIPHER_KEY_MOD
            power //= 2
            number *= number
            number %= CIPHER_KEY_MOD
        return result

    def __apply_caesar(self, delta):
        """Applies caesar cipher to the key. The characters are bound by CIPHER_KEY_ASCII_LIM.
        Args:
            delta (int): The delta by which the characters are required to be shifted.
        """
        keylist = list(self.key)
        for index in range(len(keylist)):
            keylist[index] = chr((ord(keylist[index]) + delta) %
                                 CIPHER_KEY_ASCII_LIM)
        self.key = ''.join(keylist)

    def __randomize(self):
        """Applies randomization to the characters of the key."""
        self.key = ''.join(random.sample(self.key, len(self.key)))

    def __pad(self):
        """Repeatedly appends specified master password to the key till the key is 
        of required length, i.e, CIPHER_KEY_LENGTH.
        """
        while len(self.key) + len(self.master_password) < CIPHER_KEY_LENGTH:
            self.key += self.master_password

        if len(self.key) < CIPHER_KEY_LENGTH:
            length_required = CIPHER_KEY_LENGTH - len(self.key)
            self.key += self.master_password[0: length_required]

    def __trim(self):
        """Trims the key by truncating anything beyond CIPHER_KEY_LENGTH"""
        self.key = self.key[0: CIPHER_KEY_LENGTH]

    class Builder:
        """Builder class for CipherKey

        Cipher class follows builder design pattern. 
        Attributes:
            master_password (str): Master password for key generation.
            master_key (int): Master key for key generation
        """
        master_password = None
        master_key = None

        def set_master_password(self, master_password):
            """Sets the master password for the builder.
            Args:
                master_password (str): Master password for key generation.
            """
            self.master_password = master_password

        def set_master_key(self, master_key):
            """Sets the master key for the builder.
            Args:
                master_key (int): Master key for key generation.
            """
            self.master_key = master_key

        def build(self):
            """Builds and returns an instance of CipherKey."""
            return CipherKey(self.master_password, self.master_key)
