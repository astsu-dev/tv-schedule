from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.application.models.episode import EpisodeUpdate


class IUpdateEpisodeUseCaseRepo(Protocol):
    """"""

    async def update(self, episode: EpisodeUpdate) -> None:
        """Updates episode in repo.

        Args:
            episode (EpisodeUpdate): data for updating episode in repo
        """


class UpdateEpisodeUseCase:
    """Updates tv show episode in repo"""

    def __init__(self, repo: IUpdateEpisodeUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, episode: EpisodeUpdate) -> None:
        """Updates tv show episode to repo.

        Args:
            episode (EpisodeUpdate): data for updating episode
        """

        logger = self._logger

        logger.info(f"Start updating episode {episode} in repo")

        await self._repo.update(episode)

        logger.info(f"Finish updating episode {episode} in repo")
