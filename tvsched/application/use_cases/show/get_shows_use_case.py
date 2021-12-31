from typing import Optional, Protocol

from tvsched.application.interfaces import ILogger
from tvsched.entities.show import Show


class IGetShowsUseCaseRepo(Protocol):
    async def get_shows(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[Show]:
        """Returns list of shows from repo by.

        Args:
            limit (Optional[int]): max number of shows. If None all shows will be returned
            offset (Optional[int])

        Returns:
            list[Show]
        """
        ...  # fix return type error


class GetShowsUseCase:
    def __init__(self, repo: IGetShowsUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[Show]:
        """Returns list of shows from repo by.

        Args:
            limit (Optional[int]): max number of shows. If None all shows will be returned
            offset (Optional[int])

        Returns:
            list[Show]
        """

        logger = self._logger

        logger.info(f"Start getting shows. Offset - {offset}, limit - {limit}")

        shows = await self._repo.get_shows(limit=limit, offset=offset)

        logger.info(f"Finish getting shows. Offset - {offset}, limit - {limit}")

        return shows
