from datetime import datetime, timedelta
from typing import Tuple, Union

from config import settings
from helpers.hash import create_hash
from jose import jwt


def create_access_token(id: int) -> Tuple[str, str]:
    """
    Generate a access & refresh token for the user

    Args:
        id: Manager to generate the token for

    Returns:
        Encoded token
    """
    salt, token_hash = create_hash(
        f"{settings.jwt_private_key}-REFRESH_TOKEN-{id}-{datetime.utcnow()}"
    )
    refresh_token = f"{salt}.{token_hash}"
    #User.update(id, {"refresh_token": refresh_token})
    access_token = jwt.encode(
        {"id": id, "exp": datetime.utcnow() + timedelta(seconds=settings.jwt_expiry),},
        settings.jwt_private_key,
        algorithm="RS256",
    )
    return access_token, refresh_token

def create_admin_access_token(key: str) -> Tuple[str, str]:
    """
    Generate a access & refresh token for the user

    Args:
        id: Manager to generate the token for

    Returns:
        Encoded token
    """
    salt, token_hash = create_hash(
        f"{settings.jwt_private_key}-REFRESH_TOKEN-{key}-{datetime.utcnow()}"
    )
    refresh_token = f"{salt}.{token_hash}"
    #User.update(id, {"refresh_token": refresh_token})
    access_token = jwt.encode(
        {"id": key, "exp": datetime.utcnow() + timedelta(seconds=settings.jwt_expiry),},
        settings.jwt_private_key,
        algorithm="RS256",
    )
    return access_token, refresh_token
def get_expiry_time():
    return int(datetime.utcnow().timestamp()) + (settings.jwt_expiry * 60)


def decode_token(token: str) -> Tuple[Union[int, None], str]:
    """
    Decode JWT token

    Args:
        token: JWT Token

    Returns:
        User id, Error message 
        (User id is None in case of an error)
    """
    try:
        payload = jwt.decode(token, settings.jwt_public_key, algorithms=["RS256"])
        return payload["id"], ""
    except jwt.ExpiredSignatureError:
        return None, "Expired token"
    except jwt.JWTError:
        return None, "Invalid token"
    except Exception as e:
        return None, str(e)
