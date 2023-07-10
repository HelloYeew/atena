import random


def generate_api_key() -> str:
    """
    Generate a random 32 character string mixed with letters and digits.
    :return: 32 character string
    """
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))
