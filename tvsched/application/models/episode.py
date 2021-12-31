import datetime

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class EpisodeAdd:
    """Data for adding episode to repo"""

    name: str
    season: int
    number: int
    air_date: datetime.datetime
    show_id: int


@dataclass(frozen=True)
class EpisodeUpdate:
    """Data for updating episode in repo"""

    id: int
    name: Optional[str] = None
    season: Optional[int] = None
    number: Optional[int] = None
    air_date: Optional[datetime.datetime] = None
    show_id: Optional[int] = None
