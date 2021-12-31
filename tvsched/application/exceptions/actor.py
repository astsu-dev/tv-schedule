from tvsched.application.models.actor import ActorInShowCast


class ActorNotFoundError(Exception):
    """Will be raised if actor not found in repo"""

    def __init__(self, actor_id: int) -> None:
        self._actor_id = actor_id

    @property
    def actor_id(self) -> int:
        return self._actor_id


class ActorOrShowNotFoundError(Exception):
    """Will be raised when trying to add not existed actor to show
    or actor to not existed show
    """

    def __init__(self, actor_in_cast: ActorInShowCast) -> None:
        self._actor_in_cast = actor_in_cast

    @property
    def actor_in_cast(self) -> ActorInShowCast:
        return self._actor_in_cast


class ActorAlreadyInShowCastError(Exception):
    """Will be raised when trying to again add actor to show cast to repo"""

    def __init__(self, actor_in_cast: ActorInShowCast) -> None:
        self._actor_in_cast = actor_in_cast

    @property
    def actor_in_cast(self) -> ActorInShowCast:
        return self._actor_in_cast
