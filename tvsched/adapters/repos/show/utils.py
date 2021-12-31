import itertools as it
from typing import Iterable, Sequence

from tvsched.adapters.repos.show.models import ShowRecord
from tvsched.entities.actor import Actor
from tvsched.entities.show import Show


def group_show_records(records: Iterable[ShowRecord]) -> list[list[ShowRecord]]:
    grouped_records = it.groupby(records, lambda sr: sr["id"])
    res = [list(g) for _, g in grouped_records]

    return res


def map_show_records_to_model(records: Sequence[ShowRecord]) -> Show:
    """Maps list of records of show from repo to model.

    Example:
        >>> records = [
        ... {
        ...     "id": 1,
        ...     "name": "show1",
        ...     "seasons_count": 8,
        ...     "image_url": "url1",
        ...     "actor_id": 1,
        ...     "actor_name": "actor1",
        ...     "actor_image_url": "url1",
        ... },
        ... {
        ...     "id": 1,
        ...     "name": "show1",
        ...     "seasons_count": 8,
        ...     "image_url": "url1",
        ...     "actor_id": 2,
        ...     "actor_name": "actor2",
        ...     "actor_image_url": "url2",
        ... },
        ... ]
        >>> expected = Show(
        ...    id=1,
        ...    name="show1",
        ...    seasons_count=8,
        ...    image_url="url1",
        ...    cast=[
        ...        Actor(id=1, name="actor1", image_url="url1"),
        ...        Actor(id=2, name="actor2", image_url="url2"),
        ...    ],
        ... )
        >>> assert map_show_records_to_model(records) == expected

    Args:
        records (Sequence[ShowRecord])

    Returns:
        Show
    """

    cast = [
        Actor(id=s["actor_id"], name=s["actor_name"], image_url=s["actor_image_url"])
        for s in records
    ]
    record = records[0]
    show = Show(
        id=record["id"],
        name=record["name"],
        seasons_count=record["seasons_count"],
        image_url=record["image_url"],
        cast=cast,
    )

    return show
