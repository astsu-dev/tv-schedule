from uuid import UUID


class UserNotFoundError(Exception):
    """Will be raised when user does not exist in repo."""

    def __init__(self, user_id: UUID) -> None:
        self._user_id = user_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

class UserAlreadyExistsError(Exception):
    """Will be raised when trying to add existed user to repo."""

    def __init__(self, user_id: UUID) -> None:
        self._user_id = user_id

    @property
    def user_id(self) -> UUID:
        return self._user_id
