from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class Episode:
    """TV show episode entity"""

    id: int
    name: str
    season: int
    number: int
    air_date: datetime.datetime
    show_id: int
