from typing import Protocol

from tvsched.application.exceptions.actor import (
    ActorAlreadyInShowCastError,
    ActorOrShowNotFoundError,
)
from tvsched.application.interfaces import ILogger
from tvsched.application.models.actor import ActorInShowCast


class IAddActorToShowCaseUseCaseRepo(Protocol):
    async def add_actor_to_show_cast(self, data: ActorInShowCast) -> None:
        """Adds actor to show cast in repo.

        Args:
            data (ActorInShowCast): data for adding actor to show cast
        """


class AddActorToShowCastUseCase:
    """Adds actor to show cast"""

    def __init__(self, repo: IAddActorToShowCaseUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, data: ActorInShowCast) -> None:
        """Adds actor to show cast in repo.

        Args:
            data (ActorInShowCast): data for adding actor to cast

        Raises:
            ActorAlreadyInShowCastError: will be raised if actor already exists in show cast
            ActorOrShowNotFoundError: will be raised if actor or show does not exist
        """

        logger = self._logger

        logger.info(f"Start adding actor to show cast {data} in repo")

        try:
            await self._repo.add_actor_to_show_cast(data)
        except ActorOrShowNotFoundError:
            logger.info(
                f"Not found actor with id {data.actor_id} or show with id {data.show_id}"
            )
            raise
        except ActorAlreadyInShowCastError:
            logger.info(
                f"Actor with id {data.actor_id} already exists in show cast with id {data.show_id}."
            )
            raise

        logger.info(f"Finish adding actor to show cast {data} in repo")
