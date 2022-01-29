from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.application.exceptions.auth import UserAlreadyExistsError
from tvsched.application.models.auth import UserWithRoleAdd, UserInRepo
from tvsched.application.utils.auth import hash_password


class IAddUserWithRoleUseCaseRepo(Protocol):
    """"""

    async def add_user(self, user: UserInRepo) -> None:
        """Adds user to repo.

        Args:
            user (UserInRepo): data for adding user to repo.

        Raises:
            UserAlreadyExistsError: will be raised when user already exists.
        """


class AddUserWithRoleUseCase:
    """Adds user with specific role to repo"""

    def __init__(self, repo: IAddUserWithRoleUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, user: UserWithRoleAdd) -> None:
        """Adds user with specific role to repo.

        Args:
            user (UserWithRoleAdd): data for adding user to repo.

        Raises:
            UserAlreadyExistsError: will be raised when user already exists.
        """

        logger = self._logger

        logger.info(f"Start adding user {user.username} with role {user.role} to repo")

        username = user.username

        password_hash = hash_password(user.password)

        user_in_repo = UserInRepo(
            username=user.username, password_hash=password_hash, role=user.role
        )

        try:
            await self._repo.add_user(user_in_repo)
        except UserAlreadyExistsError:
            logger.info(f"User with name {username} already exists.")
            raise

        logger.info(f"Finish adding user {user.username} with role {user.role} to repo")
