from typing import TypedDict


class ShowRecord(TypedDict):
    id: int
    name: str
    seasons_count: int
    image_url: str
    actor_id: int
    actor_name: str
    actor_image_url: str
