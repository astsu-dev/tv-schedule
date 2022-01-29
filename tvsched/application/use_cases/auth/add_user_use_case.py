from tvsched.application.interfaces import ILogger
from tvsched.application.models.auth import UserAdd, UserWithRoleAdd
from tvsched.application.use_cases.auth.add_user_with_role_use_case import (
    AddUserWithRoleUseCase,
    IAddUserWithRoleUseCaseRepo,
)
from tvsched.entities.auth import Role


class AddUserUseCase:
    """Adds user with USER role to repo."""

    def __init__(self, repo: IAddUserWithRoleUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger
        self._use_case = AddUserWithRoleUseCase(repo, logger)

    async def execute(self, user: UserAdd) -> None:
        """Adds user with USER role to repo.

        Args:
            user (UserAdd): data for adding user to repo

        Raises:
            UserAlreadyExistsError: will be raised when user already exists
        """

        user_with_role = UserWithRoleAdd(user.username, user.password, Role.USER)
        await self._use_case.execute(user_with_role)
