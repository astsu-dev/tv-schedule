from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.application.models.schedule import EpisodeInSchedule


class IMarkEpisodeAsUnwatchedUseCaseRepo(Protocol):
    """"""

    async def mark_episode_as_unwatched(
        self, episode_in_schedule: EpisodeInSchedule
    ) -> None:
        """Marks episode with `episode_id` as unwatched in repo.

        Args:
            episode_in_schedule (EpisodeInSchedule): data for marking episode as unwatched in schedule
        """


class MarkEpisodeAsUnwatchedUseCase:
    """Marks episode as unwatched in user schedule"""

    def __init__(
        self, repo: IMarkEpisodeAsUnwatchedUseCaseRepo, logger: ILogger
    ) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, episode_in_schedule: EpisodeInSchedule) -> None:
        """Marks episode as watched in user schedule

        Args:
            episode_in_schedule (EpisodeInSchedule): data for marking episode
                as unwatched in schedule
        """

        logger = self._logger
        episode_id = episode_in_schedule.episode_id
        user_id = episode_in_schedule.user_id

        logger.info(
            f"Start marking episode id {episode_id} as unwatched in schedule with user id {user_id} in repo"
        )

        await self._repo.mark_episode_as_unwatched(episode_in_schedule)

        logger.info(
            f"Finish marking episode id {episode_id} as unwatched in schedule with user id {user_id} in repo"
        )
