from typing import Protocol
import uuid

from tvsched.application.interfaces import ILogger
from tvsched.entities.episode import Episode


class IGetFirstUnwatchedEpisodesFromScheduleUseCaseRepo(Protocol):
    """"""

    async def get_first_unwatched_episodes_from_schedule(
        self, user_id: uuid.UUID
    ) -> list[Episode]:
        """Returns list of first unwatched episodes
        for each show from schedule from repo.

        Args:
            user_id (uuid.UUID): user schedule id

        Returns:
            list[Episode]
        """

        raise NotImplementedError


class GetFirstUnwatchedEpisodesFromScheduleUseCase:
    """Gets first unwatched episodes for each show from schedule"""

    def __init__(
        self, repo: IGetFirstUnwatchedEpisodesFromScheduleUseCaseRepo, logger: ILogger
    ) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, user_id: uuid.UUID) -> list[Episode]:
        """Returns list of first unwatched episodes
        for each show from schedule.

        Args:
            user_id (uuid.UUID): user schedule id

        Returns:
            list[Episode]
        """

        logger = self._logger

        logger.info(
            f"Start getting first unwatched episodes for each show in schedule with user id {user_id}"
        )

        episodes = await self._repo.get_first_unwatched_episodes_from_schedule(user_id)

        logger.info(
            f"Finish getting first unwatched episodes for each show in schedule with user id {user_id}"
        )

        return episodes
