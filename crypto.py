import base64
import os

from Crypto.Cipher import AES, DES
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
des_key = ""


def des_encrypt(message):
    des = DES.new(bytes(key, encoding="utf-8")[::2], DES.MODE_ECB)
    padded_message = message + " " * (8 - len(message) % 8)
    encrypted_message = des.encrypt(bytes(padded_message, encoding="utf-8"))
    return base64.b64encode(encrypted_message).decode()


def des_decrypt(encrypted_message):
    des = DES.new(bytes(key, encoding="utf-8")[::2], DES.MODE_ECB)
    decrypted_message = des.decrypt(
        bytes(base64.b64decode(encrypted_message), encoding="utf-8")
    ).decode()
    return decrypted_message.rstrip()


def aes_encrypt(message):
    aes = AES.new(key, AES.MODE_ECB)
    padded_message = message + " " * (16 - len(message) % 16)
    encrypted_message = aes.encrypt(padded_message.encode())
    return base64.b64encode(encrypted_message).decode()


def aes_decrypt(encrypted_message):
    aes = AES.new(key, AES.MODE_ECB)
    decrypted_message = aes.decrypt(base64.b64decode(encrypted_message)).decode()
    return decrypted_message.rstrip()


class Cipher:
    def __init__(self, encryption_function, decryption_function, description):
        self.encrypt = encryption_function
        self.decrypt = decryption_function
        self.__doc__ = description

    def verify(self, plain_text, encrypted_message, is_encrypted):
        if not is_encrypted:
            return plain_text == encrypted_message
        return plain_text == self.decrypt(encrypted_message)


AES_Cipher = Cipher(aes_encrypt, aes_decrypt, "AES Cipher")
DES_Cipher = Cipher(des_encrypt, des_decrypt, "DES Cipher")
