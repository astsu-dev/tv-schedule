from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.application.models.show import ShowUpdate


class IUpdateShowUseCaseRepo(Protocol):
    async def update(self, show: ShowUpdate) -> None:
        """Updates show in repo.

        Args:
            show (ShowUpdate): new show data
        """


class UpdateShowUseCase:
    """Updates show in repo"""

    def __init__(self, repo: IUpdateShowUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, show: ShowUpdate) -> None:
        """Updates tv show in repo.

        Args:
            show (ShowUpdate): new show data

        Raises:
            ShowNotFoundError: will be raised if show with id `show.id` not in repo
        """

        logger = self._logger

        logger.info(f"Start updating show {show} in repo")

        await self._repo.update(show)

        logger.info(f"Finish updating show {show} in repo")
