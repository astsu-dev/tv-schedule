import datetime
from typing import Protocol
from tvsched.application.exceptions.auth import (
    InvalidUserPasswordError,
    UserNotFoundError,
)

from tvsched.application.interfaces import ILogger
from tvsched.application.models.auth import UserInRepo, UserInToken, UserLogIn
from tvsched.application.utils.auth import (
    create_access_token_for_user,
    verify_password,
)


class ILogInUserUseCaseRepo(Protocol):
    """"""

    async def get_user_by_username(self, username: str) -> UserInRepo:
        """Returns user by username from repo.

        Args:
            user (UserInRepo): data for adding user to repo.

        Raises:
            UserAlreadyExistsError: will be raised when user already exists.

        Returns:
            UserInRepo
        """

        raise NotImplementedError  # fix return type error


class LogInUserUseCase:
    """Generates token for user."""

    def __init__(
        self,
        repo: ILogInUserUseCaseRepo,
        logger: ILogger,
        jwt_secret: str,
        jwt_expires_in: datetime.timedelta,
        jwt_algorithm: str,
    ) -> None:
        self._repo = repo
        self._logger = logger
        self._jwt_secret = jwt_secret
        self._jwt_expires_in = jwt_expires_in
        self._jwt_algorithm = jwt_algorithm

    async def execute(self, user: UserLogIn) -> str:
        """Log in user.

        Generates token.

        Args:
            user (UserLogIn): data for adding user to repo.

        Raises:
            UserNotFoundError: will be raised when user with `username` does not exist.

        Returns:
            str: access token
        """

        repo = self._repo
        logger = self._logger

        username = user.username
        logger.info(f"Start log in user with username {username}")

        try:
            user_in_repo = await repo.get_user_by_username(username)
        except UserNotFoundError:
            logger.info("Not found user with username {username}")
            raise

        if not verify_password(user.password, user_in_repo.password_hash):
            logger.info("Invalid password for username {username}")
            raise InvalidUserPasswordError(username=username)

        user_in_token = UserInToken(id=user_in_repo.id, role=user_in_repo.role)
        created_at = datetime.datetime.utcnow()
        token = create_access_token_for_user(
            user=user_in_token,
            created_at=created_at,
            key=self._jwt_secret,
            expires_in=self._jwt_expires_in,
            algorithm=self._jwt_algorithm,
        )

        logger.info(f"Finish log in user with username {username}")

        return token
