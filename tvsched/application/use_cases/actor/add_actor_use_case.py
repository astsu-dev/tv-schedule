from typing import Protocol
from tvsched.application.interfaces import ILogger

from tvsched.application.models.actor import ActorAdd


class IAddActorUseCaseRepo(Protocol):
    async def add(self, actor: ActorAdd) -> None:
        """Adds actor to repo.

        Args:
            actor (ActorAdd): data for adding actor
        """


class AddActorUseCase:
    """Adds actor to repo"""

    def __init__(self, repo: IAddActorUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, actor: ActorAdd) -> None:
        """Adds actor to repo.

        Args:
            actor (ActorAdd): data for adding actor
        """

        logger = self._logger

        logger.info(f"Start adding actor {actor} to repo")

        await self._repo.add(actor)

        logger.info(f"Finish adding actor {actor} to repo")
