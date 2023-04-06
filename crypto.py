import base64
import os

from Crypto.Cipher import AES
from dotenv import load_dotenv

load_dotenv("./.env")


def load_key():
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("No secret key set for encryption")
    if len(key) != 16:
        raise ValueError("Secret key must be 16 bytes long")
    return key.encode()


key = load_key()


def encrypt(message):
    aes = AES.new(key, AES.MODE_ECB)
    padded_message = message + " " * (16 - len(message) % 16)
    encrypted_message = aes.encrypt(padded_message.encode())
    return base64.b64encode(encrypted_message).decode()


def decrypt(encrypted_message):
    aes = AES.new(key, AES.MODE_ECB)
    decrypted_message = aes.decrypt(base64.b64decode(encrypted_message)).decode()
    return decrypted_message.rstrip()


def verify(plain_text, encrypted_message, is_encrypted):
    if not is_encrypted:
        return plain_text == encrypted_message
    return plain_text == decrypt(encrypted_message)


class Cipher:
    def __init__(self, encryption_function, decryption_function, description):
        self.encrypt = encryption_function
        self.decrypt = decryption_function
        self.__doc__ = description
