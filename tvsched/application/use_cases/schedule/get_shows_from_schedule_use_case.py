import uuid
from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.entities.show import Show


class IGetShowsFromScheduleUseCaseRepo(Protocol):
    async def get_shows_from_schedule(self, user_id: uuid.UUID) -> list[Show]:
        """Returns list of shows from user schedule.

        Args:
            user_id (uuid.UUID): user schedule user user_id

        Returns:
            list[Show]
        """
        ...  # fix return type error


class GetShowsFromScheduleUseCase:
    """Gets shows from user schedule from repo"""

    def __init__(self, repo: IGetShowsFromScheduleUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, user_id: uuid.UUID) -> list[Show]:
        """Returns list of tv shows from user schedule with user id `user_id`.

        Args:
            user_id (uuid.UUID): user schedule id

        Returns:
            list[Show]
        """

        logger = self._logger

        logger.info(f"Start getting shows in schedule with user id {user_id}")

        shows = await self._repo.get_shows_from_schedule(user_id)

        logger.info(f"Finish getting shows in schedule with user id {user_id}")

        return shows
