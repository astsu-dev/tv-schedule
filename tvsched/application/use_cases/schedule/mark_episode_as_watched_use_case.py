from typing import Protocol

from tvsched.application.exceptions.schedule import (
    EpisodeAlreadyMarkedAsWatchedError,
    EpisodeOrScheduleNotFoundError,
)
from tvsched.application.interfaces import ILogger
from tvsched.application.models.schedule import EpisodeInSchedule


class IMarkEpisodeAsWatchedUseCaseRepo(Protocol):
    """"""

    async def mark_episode_as_watched(
        self, episode_in_schedule: EpisodeInSchedule
    ) -> None:
        """Marks episode with `episode_id` as watched in repo.

        Args:
            episode_in_schedule (EpisodeInSchedule): data for marking episode
                as watched in schedule

        Raises:
            EpisodeOrScheduleNotFoundError: will be raised if episode or schedule does not exists
            EpisodeAlreadyExistsInScheduleError: will be raised if episode already marked as watched in schedule
        """


class MarkEpisodeAsWatchedUseCase:
    """Marks episode as watched in user schedule"""

    def __init__(self, repo: IMarkEpisodeAsWatchedUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, episode_in_schedule: EpisodeInSchedule) -> None:
        """Marks episode as watched in user schedule

        Args:
            episode_in_schedule (EpisodeInSchedule): data for marking episode
                as watched in schedule

        Raises:
            EpisodeOrScheduleNotFoundError: will be raised if episode or schedule does not exists
            EpisodeAlreadyExistsInScheduleError: will be raised if episode already marked as watched in schedule
        """

        logger = self._logger
        episode_id = episode_in_schedule.episode_id
        user_id = episode_in_schedule.user_id

        logger.info(
            f"Start marking episode id {episode_id} as watched in schedule with user id {user_id} in repo"
        )

        try:
            await self._repo.mark_episode_as_watched(episode_in_schedule)
        except EpisodeOrScheduleNotFoundError:
            logger.info(
                f"Not found episode with id {episode_id} or schedule with user id {user_id} in repo"
            )
            raise
        except EpisodeAlreadyMarkedAsWatchedError:
            logger.info(
                f"Episode with id {episode_id} already mark as watched in schedule with user id {user_id}"
            )
            raise

        logger.info(
            f"Finish marking episode id {episode_id} as watched in schedule with user id {user_id} in repo"
        )
