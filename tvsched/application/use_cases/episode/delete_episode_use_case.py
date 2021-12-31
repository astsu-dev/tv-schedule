from typing import Protocol

from tvsched.application.interfaces import ILogger


class IDeleteEpisodeUseCaseRepo(Protocol):
    """"""

    async def delete(self, episode_id: int) -> None:
        """Deletes episode with `episode_id` from repo.

        Args:
            episode (EpisodeDelete): data for adding episode to repo
        """


class DeleteEpisodeUseCase:
    """Deletes tv episode to repo"""

    def __init__(self, repo: IDeleteEpisodeUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, episode_id: int) -> None:
        """Deletes tv episode from repo with `episode_id`.

        Args:
            episode_id (int)
        """

        logger = self._logger

        logger.info(f"Start deleting episode with episode id {episode_id} from repo")

        await self._repo.delete(episode_id)

        logger.info(f"Finish deleting episode with episode id {episode_id} from repo")
