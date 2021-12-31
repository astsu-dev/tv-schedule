import uuid
from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.entities.show import Show


class IGetSuggestedShowsUseCaseRepo(Protocol):
    async def get_suggested_shows(self, user_id: uuid.UUID) -> list[Show]:
        """Returns list of suggested tv shows based on show cast
        for schedule with user id `user_id`.

        Args:
            user_id (uuid.UUID): user schedule user id

        Returns:
            list[Show]
        """
        ...  # fix return type error


class GetSuggestedShowsUseCase:
    def __init__(self, repo: IGetSuggestedShowsUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, user_id: uuid.UUID) -> list[Show]:
        """Returns list of suggested tv shows based on show cast
        for schedule with user id `user_id`.

        Args:
            user_id (uuid.UUID): user schedule user id

        Returns:
            list[Show]
        """

        logger = self._logger

        logger.info(f"Start getting suggested show for user with user id {user_id}")

        show = await self._repo.get_suggested_shows(user_id)

        logger.info(f"Finish getting suggested show for user with user id {user_id}")

        return show
