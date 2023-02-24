from hashlib import sha256
import secrets


def hasher(text: str) -> str:
    """
    Takes a UTF-8 encoded piece of text of any length, and returns the SHA-256 hash of the text as a string object, in uppercase.
    """
    return sha256(bytes(text, "utf-8")).hexdigest().upper()

def salter() -> str:
    """
    Returns the base64 encoded string of the text,
    """
    return secrets.token_hex(8)

def encrypt(text : str) -> str:
    """
    Returns a SHA-256 hash of the text
    """
    salt = salter()
    return f"{hasher(text+salt)}#{salt}"

def verify(text : str,hash : str,isEncypted : bool):
    if not isEncypted:
        return text == hash
    else:
        hashed,salt = hash.split("#")
        return hasher(text + salt) == hashed