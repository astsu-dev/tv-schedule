from typing import Protocol
from tvsched.application.exceptions.show import ShowNotFoundError

from tvsched.application.interfaces import ILogger
from tvsched.entities.show import Show


class IGetShowUseCaseRepo(Protocol):
    async def get(self, show_id: int) -> Show:
        """Returns show from repo by `show_id`.

        Args:
            show_id (show)

        Raises:
            ShowNotFoundError: will be raised if show with id `show_id` not in repo

        Returns:
            Show
        """
        ...  # fix return type error


class GetShowUseCase:
    def __init__(self, repo: IGetShowUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, show_id: int) -> Show:
        """Returns tv show from repo.

        Args:
            show_id (int)

        Raises:
            ShowNotFound: raises if show with id `show_id` not in repo

        Returns:
            Show
        """

        logger = self._logger

        logger.info(f"Start getting show with id {show_id}")

        try:
            show = await self._repo.get(show_id)
        except ShowNotFoundError:
            logger.info(f"Not found show with id {show_id}")
            raise

        logger.info(f"Finish getting show with id {show_id}")

        return show
