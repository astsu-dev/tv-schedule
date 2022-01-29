from passlib.hash import bcrypt


def hash_password(password: str) -> str:
    """Returns password hashed by bcrypt algorithm.

    Args:
        password (str)

    Returns:
        str
    """

    return bcrypt.hash(password)
