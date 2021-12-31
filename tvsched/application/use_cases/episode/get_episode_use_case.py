from typing import Protocol

from tvsched.application.exceptions.episode import EpisodeNotFoundError
from tvsched.application.interfaces import ILogger
from tvsched.entities.episode import Episode


class IGetEpisodeUseCaseRepo(Protocol):
    """"""

    async def get(self, episode_id: int) -> Episode:
        """Returns episode with `episode_id` from repo.

        Args:
            episode_id (int)

        Returns:
            Episode
        """

        raise NotImplementedError


class GetEpisodeUseCase:
    """Gets tv show episode"""

    def __init__(self, repo: IGetEpisodeUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, episode_id: int) -> Episode:
        """Returns episode with `episode_id` from repo.

        Args:
            episode_id (int)

        Raises:
            EpisodeNotFoundError: will be raised if show not exists

        Returns:
            list[Episode]
        """

        logger = self._logger

        logger.info(f"Start getting episode with id {episode_id}")

        try:
            episode = await self._repo.get(episode_id)
        except EpisodeNotFoundError:
            logger.info(f"Not found episode with id {episode_id} in repo")
            raise

        logger.info(f"Finish getting episode with id {episode_id}")

        return episode
