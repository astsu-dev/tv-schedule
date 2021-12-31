from typing import Protocol

from tvsched.application.interfaces import ILogger


class IDeleteShowUseCaseRepo(Protocol):
    async def delete(self, show_id: int) -> None:
        """Deletes show `show_id` from repo.

        Args:
            show_id (int)
        """


class DeleteShowUseCase:
    def __init__(self, repo: IDeleteShowUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, show_id: int) -> None:
        """Deletes tv show from repo.

        Args:
            show_id (int)
        """

        logger = self._logger

        logger.info(f"Start deleting show with id {show_id} to repo")

        await self._repo.delete(show_id)

        logger.info(f"Finish deleting show with id {show_id} to repo")
