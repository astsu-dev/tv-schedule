from typing import Protocol

from tvsched.application.exceptions.schedule import (
    ShowOrScheduleNotFoundError,
    ShowAlreadyExistsInScheduleError,
)
from tvsched.application.interfaces import ILogger
from tvsched.application.models.schedule import ShowInSchedule


class IAddShowToScheduleUseCaseRepo(Protocol):
    async def add_to_schedule(self, data: ShowInSchedule) -> None:
        """Adds show to user schedule in repo.

        Args:
            data (ShowInSchedule): data for adding show to user schedule
        """


class AddShowToScheduleUseCase:
    """Adds show to user schedule in repo"""

    def __init__(self, repo: IAddShowToScheduleUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, data: ShowInSchedule) -> None:
        """Adds tv show to user schedule.

        Args:
            data (ShowInSchedule): data for adding show to schedule

        Raises:
            ShowNotFoundError: will be raised if show with
                id `data.show_id` not in repo
            ShowAlreadyExistsInScheduleError: will be raised when trying to
                add already existed in schedule show to schedule
        """

        logger = self._logger

        logger.info(
            f"Start adding show with {data.show_id} show id to user schedule with {data.user_id} user id"
        )

        try:
            await self._repo.add_to_schedule(data)
        except ShowAlreadyExistsInScheduleError:
            logger.info(
                f"Show with id {data.show_id} already in schedule with user id {data.user_id}"
            )
            raise
        except ShowOrScheduleNotFoundError:
            logger.info(
                f"Show with id {data.show_id} or schedule with user id {data.user_id} doest not exist"
            )
            raise

        logger.info(
            f"Finish adding show with {data.show_id} show id to user schedule with {data.user_id} user id"
        )
