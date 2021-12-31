from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.application.models.actor import ActorUpdate


class IUpdateActorUseCaseRepo(Protocol):
    async def update(self, actor: ActorUpdate) -> None:
        """Updates actor in repo.

        Args:
            actor (ActorUpdate): data for updating actor
        """


class UpdateActorUseCase:
    """Updates actor in repo"""

    def __init__(self, repo: IUpdateActorUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, actor: ActorUpdate) -> None:
        """Updates actor to repo.

        Args:
            actor (ActorUpdate): data for updating actor
        """

        logger = self._logger

        logger.info(f"Start updating actor {actor} to repo")

        await self._repo.update(actor)

        logger.info(f"Finish updating actor {actor} to repo")
