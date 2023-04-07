import base64
import os

from Crypto.Cipher import AES, DES, Blowfish
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv

load_dotenv(os.path.dirname(__file__) + "/./.env")


def load_key():
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("No secret key set for encryption")
    if len(key) != 16:
        raise ValueError("Secret key must be 16 bytes long")
    return key.encode()


key = load_key()


def des_encrypt(message):
    """
    Encrypts a message using the DES algorithm in ECB mode.
    """
    # Create a new DES object with the key and mode
    des = DES.new(key[::2], DES.MODE_ECB)
    # Pad the message to a multiple of 8 bytes using spaces
    padded_message = message + " " * (8 - len(message) % 8)
    # Encrypt the padded message using DES
    encrypted_message = des.encrypt(bytes(padded_message, encoding="utf-8"))
    # Encode the encrypted message in base64 and return as a string
    return base64.b64encode(encrypted_message).decode()


def des_decrypt(encrypted_message):
    """
    Decrypts an encrypted message using the DES algorithm in ECB mode.
    """
    # Create a new DES object with the key and mode
    des = DES.new(key[::2], DES.MODE_ECB)
    # Decode the encrypted message from base64
    decoded_message = base64.b64decode(encrypted_message)
    # Decrypt the decoded message using DES
    decrypted_message = des.decrypt(decoded_message).decode()
    # Remove any trailing whitespace from the decrypted message and return
    return decrypted_message.rstrip()


def aes_encrypt(message):
    """
    Encrypts a message using the AES algorithm in ECB mode.
    """
    # Create a new AES object with the key and mode
    aes = AES.new(key, AES.MODE_ECB)
    # Pad the message to a multiple of 16 bytes using spaces
    padded_message = message + " " * (16 - len(message) % 16)
    # Encrypt the padded message using AES
    encrypted_message = aes.encrypt(padded_message.encode())
    # Encode the encrypted message in base64 and return as a string
    return base64.b64encode(encrypted_message).decode()


def aes_decrypt(encrypted_message):
    """
    Decrypts an encrypted message using the AES algorithm in ECB mode.
    """
    # Create a new AES object with the key and mode
    aes = AES.new(key, AES.MODE_ECB)
    # Decode the encrypted message from base64
    decoded_message = base64.b64decode(encrypted_message)
    # Decrypt the decoded message using AES
    decrypted_message = aes.decrypt(decoded_message).decode()
    # Remove any trailing whitespace from the decrypted message and return
    return decrypted_message.rstrip()


def caesar_encrypt(message):
    """
    Encrypts a message using the Caesar cipher with the given key.
    """

    result = ""
    for char in message:
        # Check if character is a letter
        if char.isalpha():
            # Convert to uppercase
            char = char.upper()
            # Apply shift based on key
            shifted_char = chr((ord(char) - 65 + len(str(key))) % 26 + 65)
            # Add shifted character to result
            result += shifted_char
        else:
            # Add non-letter character as is
            result += char
    return result


def caesar_decrypt(message):
    """
    Decrypts a message using the Caesar cipher with the given key.
    """
    result = ""
    for char in message:
        # Check if character is a letter
        if char.isalpha():
            # Convert to uppercase
            char = char.upper()
            # Apply reverse shift based on key
            shifted_char = chr((ord(char) - 65 - len(str(key))) % 26 + 65)
            # Add shifted character to result
            result += shifted_char
        else:
            # Add non-letter character as is
            result += char
    return result


def blowfish_encrypt(plaintext):
    # Create a new instance of the Blowfish cipher with the provided key and ECB mode
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    # Pad the plaintext to match the block size of the cipher
    padded_plaintext = pad(plaintext.encode(), Blowfish.block_size)
    # Encrypt the padded plaintext using the Blowfish cipher
    encrypted_plaintext = cipher.encrypt(padded_plaintext)
    # Encode the encrypted plaintext using base64 and return the result
    encoded_plaintext = base64.b64encode(encrypted_plaintext).decode()
    return encoded_plaintext


def blowfish_decrypt(encoded_plaintext):
    # Create a new instance of the Blowfish cipher with the provided key and ECB mode
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    # Decode the base64-encoded encrypted plaintext
    encrypted_plaintext = base64.b64decode(encoded_plaintext)
    # Decrypt the encrypted plaintext using the Blowfish cipher
    padded_plaintext = cipher.decrypt(encrypted_plaintext)
    # Unpad the decrypted plaintext and decode it to return the result
    plaintext = unpad(padded_plaintext, Blowfish.block_size).decode()
    return plaintext


class Cipher:
    def __init__(self, encryption_function, decryption_function, description):
        self.encrypt = encryption_function
        self.decrypt = decryption_function
        self.__doc__ = description
        if not self.testing():
            raise Exception(
                self.__doc__
                + " does not seem to be a working decrypt and encrypt functions. Please check the code"
            )

    def testing(self) -> bool:
        msg = "vishal"
        if self.decrypt(self.encrypt(msg)).casefold() == msg.casefold():
            return True
        return False

    def verify(self, plain_text, encrypted_message, is_encrypted):
        if not is_encrypted:
            return plain_text == encrypted_message
        return plain_text.casefold() == self.decrypt(encrypted_message).casefold()


AES_Cipher = Cipher(aes_encrypt, aes_decrypt, "AES Cipher")
DES_Cipher = Cipher(des_encrypt, des_decrypt, "DES Cipher")
Caesar_Cipher = Cipher(caesar_encrypt, caesar_decrypt, "Caesar Cipher")
Blowfish_Cipher = Cipher(blowfish_encrypt,blowfish_decrypt,"Blowfish Cipher")