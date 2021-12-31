from typing import Protocol

from tvsched.application.exceptions.actor import ActorNotFoundError
from tvsched.application.interfaces import ILogger
from tvsched.entities.actor import Actor


class IGetActorUseCaseRepo(Protocol):
    async def get(self, actor_id: int) -> Actor:
        """Gets actor by {actor_id} from repo.

        Args:
            actor_id (id)

        Raises:
            ActorNotFoundError: will be raised if actor not found in repo

        Returns:
            Actor
        """

        raise NotImplementedError


class GetActorUseCase:
    """Gets actor in repo"""

    def __init__(self, repo: IGetActorUseCaseRepo, logger: ILogger) -> None:
        self._repo = repo
        self._logger = logger

    async def execute(self, actor_id: int) -> Actor:
        """Gets actor by {actor_id} from repo.

        Args:
            actor_id (id)

        Raises:
            ActorNotFoundError: will be raised if actor not found in repo

        Returns:
            Actor
        """

        logger = self._logger

        logger.info(f"Start getting actor with id {actor_id} from repo")

        try:
            actor = await self._repo.get(actor_id)
        except ActorNotFoundError:
            logger.info(f"Not found actor with id {actor_id} in repo")
            raise

        logger.info(f"Finish getting actor with id {actor_id} from repo")

        return actor
