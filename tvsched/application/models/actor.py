from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ActorInShowCast:
    """Data for adding actor to show cast"""

    show_id: int
    actor_id: int


@dataclass(frozen=True)
class ActorAdd:
    """Data for adding actor to repo"""

    name: str
    image_url: str


@dataclass(frozen=True)
class ActorUpdate:
    """Data for updating actor in repo"""

    id: int
    name: Optional[str] = None
    image_url: Optional[str] = None
