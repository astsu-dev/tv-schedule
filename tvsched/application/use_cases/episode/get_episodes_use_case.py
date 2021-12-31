from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.entities.episode import Episode


class IGetEpisodesFromShowUseCaseRepo(Protocol):
    """"""

    async def get_episodes_from_show(self, show_id: int) -> list[Episode]:
        """Returns list of tv show episodes with `show_id` from repo.

        Args:
            show_id (int)

        Returns:
            list[Episode]
        """

        raise NotImplementedError


class GetEpisodesFromShowUseCase:
    """Gets tv show episodes"""

    def __init__(self, repo: IGetEpisodesFromShowUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, show_id: int) -> list[Episode]:
        """Returns list of tv show episodes with `show_id` from repo.

        Args:
            show_id (int)

        Returns:
            list[Episode]
        """

        logger = self._logger

        logger.info(f"Start getting episodes from show with id {show_id}")

        episodes = await self._repo.get_episodes_from_show(show_id)

        logger.info(f"Finish getting episodes from show with id {show_id}")

        return episodes
