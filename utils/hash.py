import hashlib


def generate_hash(text):
    """Generates SHA2 as hex string. Uses internal hashlib.
    Args:
        text (str): The text whose hex is to be ca
    Returns:
        str: SHA2 string as hex characters
    """
    return hashlib.sha256(text.encode()).hexdigest()
