import uuid

from dataclasses import dataclass


@dataclass(frozen=True)
class ShowInSchedule:
    """Data for adding/deleting show to/from user schedule"""

    show_id: int
    user_id: uuid.UUID


@dataclass(frozen=True)
class EpisodeInSchedule:
    """Data for marking/unmarking episode as watched/unwatched"""

    episode_id: int
    user_id: uuid.UUID
