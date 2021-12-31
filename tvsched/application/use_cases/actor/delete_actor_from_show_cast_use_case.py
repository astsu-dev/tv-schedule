from typing import Protocol

from tvsched.application.interfaces import ILogger
from tvsched.application.models.actor import ActorInShowCast


class IDeleteActorFromShowCastUseCaseRepo(Protocol):
    async def delete_actor_from_show_cast(self, data: ActorInShowCast) -> None:
        """Deletes actor from show cast in repo.

        Args:
            data (ActorInShowCast): data for deleting actor from show cast
        """


class DeleteActorFromShowCastUseCase:
    """Deletes actor from show cast in repo"""

    def __init__(
        self, repo: IDeleteActorFromShowCastUseCaseRepo, logger: ILogger
    ) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, data: ActorInShowCast) -> None:
        """Deletes actor from show cast in repo.

        Args:
            data (ActorInShowCast): data for deleting actor to cast
        """

        logger = self._logger

        logger.info(f"Start deleting actor from show cast {data} in repo")

        await self._repo.delete_actor_from_show_cast(data)

        logger.info(f"Finish deleting actor to show cast {data} in repo")
