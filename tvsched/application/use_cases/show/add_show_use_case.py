from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.application.models.show import ShowAdd


class IAddShowUseCaseRepo(Protocol):
    """"""

    async def add(self, show: ShowAdd) -> None:
        """Adds show to repo.

        Args:
            show (ShowAdd): data for adding show to repo
        """


class AddShowUseCase:
    """Adds tv show to repo"""

    def __init__(self, repo: IAddShowUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, show: ShowAdd) -> None:
        """Adds tv show to repo.

        Args:
            show (ShowAdd): info about show

        """

        logger = self._logger

        logger.info(f"Start adding show {show} to repo")

        await self._repo.add(show)

        logger.info(f"Finish adding show {show} to repo")
