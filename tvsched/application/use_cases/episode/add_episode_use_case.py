from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.application.models.episode import EpisodeAdd


class IAddEpisodeUseCaseRepo(Protocol):
    """"""

    async def add(self, episode: EpisodeAdd) -> None:
        """Adds episode to repo.

        Args:
            episode (EpisodeAdd): data for adding episode to repo
        """


class AddEpisodeUseCase:
    """Adds tv episode to repo"""

    def __init__(self, repo: IAddEpisodeUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, episode: EpisodeAdd) -> None:
        """Adds tv episode to repo.

        Args:
            episode (EpisodeAdd): info about episode
        """

        logger = self._logger

        logger.info(f"Start adding episode {episode} to repo")

        await self._repo.add(episode)

        logger.info(f"Finish adding episode {episode} to repo")
