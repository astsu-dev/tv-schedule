from dataclasses import dataclass
import uuid

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
class UserLogIn:
    """Data for log in user"""

    username: str
    password: str


@dataclass(frozen=True)
class UserInRepoAdd:
    """Data for adding user to repo."""

    username: str
    password_hash: str
    role: Role


@dataclass(frozen=True)
class UserInRepo:
    """Data in repo about user."""

    id: uuid.UUID
    username: str
    password_hash: str
    role: Role


@dataclass(frozen=True)
class UserInToken:
    """Data about user in stored in token."""

    id: uuid.UUID
    role: Role
