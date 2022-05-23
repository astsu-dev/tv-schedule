import dataclasses
import datetime
from typing import Any

import jwt
from passlib.hash import bcrypt

from tvsched.application.models.auth import UserInToken


def hash_password(password: str) -> str:
    """Returns password hashed by bcrypt algorithm.

    Args:
        password (str)

    Returns:
        str
    """

    return bcrypt.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Returns True if password is valid.

    Args:
        password (str)
        password_hash (str)

    Returns:
        bool
    """

    return bcrypt.verify(password, password_hash)


def create_access_token(
    payload: dict[str, Any],
    created_at: datetime.datetime,
    key: str,
    expires_in: datetime.timedelta,
    algorithm: str,
) -> str:
    """Creates jwt access token.

    Adds iat, exp claims.

    Args:
        payload (dict[str, Any]): data for encoding.
        created_at (datetime.datetime): date of creation token.
        key (str): jwt secret key.
        expires_in (datetime.timedelta): token life time.
        algorithm (str): jwt algorithm.

    Returns:
        str: jwt token
    """

    expires_at = created_at + expires_in
    payload = {**payload, "iat": created_at, "exp": expires_at}
    token = jwt.encode(payload, key, algorithm=algorithm)

    return token


def create_access_token_for_user(
    user: UserInToken,
    created_at: datetime.datetime,
    key: str,
    expires_in: datetime.timedelta,
    algorithm: str,
) -> str:
    """Creates jwt access token for user.

    Args:
        user (UserInToken): data about user.
        created_at (datetime.datetime): date of creation token.
        key (str): jwt secret key.
        expires_in (datetime.timedelta): token life time.
        algorithm (str): jwt algorithm.

    Returns:
        str: jwt token
    """

    user_id = str(user.id)
    payload = {"user": {**dataclasses.asdict(user), "id": user_id}, "sub": user_id}
    token = create_access_token(
        payload,
        created_at=created_at,
        key=key,
        expires_in=expires_in,
        algorithm=algorithm,
    )

    return token
