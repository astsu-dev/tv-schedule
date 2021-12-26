from dataclasses import dataclass


@dataclass(frozen=True)
class Actor:
    """TV show cast member"""

    id: int
    name: str
    image_url: str
