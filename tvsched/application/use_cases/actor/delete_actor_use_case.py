from typing import Protocol

from tvsched.application.interfaces import ILogger


class IDeleteActorUseCaseRepo(Protocol):
    async def delete(self, actor_id: int) -> None:
        """Deletes actor by {actor_id} from repo.

        Args:
            actor_id (id)
        """


class DeleteActorUseCase:
    """Deletes actor in repo"""

    def __init__(self, repo: IDeleteActorUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, actor_id: int) -> None:
        """Deletes actor by {actor_id} from repo.

        Args:
            actor_id (id)
        """

        logger = self._logger

        logger.info(f"Start deleting actor with id {actor_id} from repo")

        await self._repo.delete(actor_id)

        logger.info(f"Finish deleting actor with id {actor_id} from repo")
