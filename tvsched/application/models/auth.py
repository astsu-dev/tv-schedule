from dataclasses import dataclass

from tvsched.entities.auth import Role


@dataclass(frozen=True)
class UserAdd:
    """Data for register user with USER role."""

    username: str
    password: str


@dataclass(frozen=True)
class UserWithRoleAdd:
    """Data for register user with specific role."""

    username: str
    password: str
    role: Role


@dataclass(frozen=True)
class UserInRepo:
    """Data for adding user to repo."""

    username: str
    password_hash: str
    role: Role
