from typing import TypedDict


class EpisodeRecord(TypedDict):
    id: int
    name: str
    season: int
    number: int
    air_date: int
    show_id: int
