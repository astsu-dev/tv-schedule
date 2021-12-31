from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.application.models.schedule import ShowInSchedule


class IDeleteShowFromScheduleUseCaseRepo(Protocol):
    async def delete_from_schedule(self, data: ShowInSchedule) -> None:
        """Deletes show from user schedule in repo.

        Args:
            data (ShowInSchedule): data for deleting show from user schedule
        """


class DeleteShowFromScheduleUseCase:
    """Deletes show from user schedule from repo"""

    def __init__(
        self, repo: IDeleteShowFromScheduleUseCaseRepo, logger: ILogger
    ) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, data: ShowInSchedule) -> None:
        """Removes tv show from user schedule.

        Args:
            data (ShowInSchedule): data for deleting tv show from schedule
        """

        logger = self._logger

        logger.info(
            f"Start deleting show with {data.show_id} show id to user schedule with {data.user_id} user id"
        )

        await self._repo.delete_from_schedule(data)

        logger.info(
            f"Finish deleting show with show id {data.show_id} to user schedule with user id {data.user_id}"
        )
