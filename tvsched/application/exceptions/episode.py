from tvsched.application.models.episode import EpisodeAdd


class EpisodeAlreadyExistsError(Exception):
    """Will be raised when trying to add existing episode to repo"""

    def __init__(self, episode: EpisodeAdd) -> None:
        self._episode = episode

    @property
    def episode(self) -> EpisodeAdd:
        return self._episode


class EpisodeNotFoundError(Exception):
    """Will be raised when trying to delete episode that not exists in repo"""

    def __init__(self, episode_id: int) -> None:
        self._episode_id = episode_id

    @property
    def episode_id(self) -> int:
        return self._episode_id
