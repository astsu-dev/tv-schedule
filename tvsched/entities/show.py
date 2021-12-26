from dataclasses import dataclass

from tvsched.entities.actor import Actor


@dataclass(frozen=True)
class Show:
    """TV show entity."""

    id: int
    name: str
    seasons_count: int
    image_url: str
    cast: list[Actor]
