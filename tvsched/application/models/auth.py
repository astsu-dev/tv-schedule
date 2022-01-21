from dataclasses import dataclass


@dataclass(frozen=True)
class UserAdd:
    """Data for register user to repo."""

    username: str
    password: str


@dataclass(frozen=True)
class UserInRepo:
    """Data for adding user to repo."""

    username: str
    password_hash: str
