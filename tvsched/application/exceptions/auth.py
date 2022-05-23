class UserNotFoundError(Exception):
    """Will be raised when user does not exist in repo."""

    def __init__(self, username: str) -> None:
        self._username = username

    @property
    def username(self) -> str:
        return self._username


class UserAlreadyExistsError(Exception):
    """Will be raised when trying to add existed user to repo."""

    def __init__(self, username: str) -> None:
        self._username = username

    @property
    def username(self) -> str:
        return self._username


class InvalidUserPasswordError(Exception):
    """Will be raised if user enter invalid password."""

    def __init__(self, username: str) -> None:
        self._username = username

    @property
    def username(self) -> str:
        return self._username
