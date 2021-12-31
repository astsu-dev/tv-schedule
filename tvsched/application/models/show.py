from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ShowAdd:
    """Data for adding show to repo"""

    name: str
    seasons_count: int
    image_url: str


@dataclass(frozen=True)
class ShowUpdate:
    """Data for updating show in repo"""

    id: int
    name: Optional[str] = None
    seasons_count: Optional[int] = None
    image_url: Optional[str] = None
