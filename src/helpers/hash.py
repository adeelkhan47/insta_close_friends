import base64
import binascii
import hashlib
import hmac
import logging
import os
from typing import Tuple


def create_hash(string: str) -> Tuple[str, str]:
    """
    Hash the provided string with a randomly-generated salt and return the
    salt and hash.

    Args:
        string: string to hash

    Returns:
        hashed string
    """
    salt = os.urandom(16)
    pw_hash = hashlib.pbkdf2_hmac("sha256", string.encode(), salt, 100000)
    salt = base64.urlsafe_b64encode(salt).decode("utf-8")
    pw_hash = base64.urlsafe_b64encode(pw_hash).decode("utf-8")
    return salt, pw_hash


def is_correct(salt: str, pw_hash: str, string: str) -> bool:
    """
    Given a previously-stored salt and hash, and a string to check against
    check whether the string is correct.

    Args:
        salt: salt
        pw_hash: hash
        string: string to check

    Returns:
        True or False
    """
    try:
        salt = base64.urlsafe_b64decode(salt.encode("utf-8"))
        pw_hash = base64.urlsafe_b64decode(pw_hash.encode("utf-8"))
        return hmac.compare_digest(
            pw_hash, hashlib.pbkdf2_hmac("sha256", string.encode(), salt, 100000)
        )
    except binascii.Error as ex:
        logging.error(f"Bad base-64 string, probably {ex}")
        return False
