import typing

from databases.core import Connection

from tvsched.adapters.repos.episode.models import EpisodeRecord
from tvsched.adapters.repos.episode.utils import (
    map_episode_record_to_model,
)
from tvsched.application.exceptions.episode import EpisodeNotFoundError
from tvsched.application.models.episode import EpisodeAdd, EpisodeUpdate
from tvsched.entities.episode import Episode


class EpisodeRepo:
    def __init__(self, db: Connection) -> None:
        self._db = db

    async def get(self, episode_id: int) -> Episode:
        """Returns episode from repo by `episode_id`.

        Args:
            episode_id (int)

        Raises:
            EpisodeNotFoundError: will be raised if episode with id `episode_id` not in repo

        Returns:
            Episode
        """

        query = """
        SELECT * FROM episodes
        WHERE id = :id;
        """

        values = dict(id=episode_id)
        record = await self._db.fetch_one(query, values=values)

        if record is None:
            raise EpisodeNotFoundError(episode_id=episode_id)

        episode_record = typing.cast(EpisodeRecord, record)
        episode = map_episode_record_to_model(episode_record)

        return episode

    async def get_episodes(self, show_id: int) -> list[Episode]:
        """Returns list of tv show episodes with tv show id `show_id`.

        Args:
            show_id (int)

        Returns:
            list[Episode]
        """

        query = """
        SELECT * FROM episodes
        WHERE show_id = :show_id;
        """

        values = dict(show_id=show_id)
        records = await self._db.fetch_all(query, values=values)

        records = typing.cast(list[EpisodeRecord], records)
        episodes = [map_episode_record_to_model(r) for r in records]

        return episodes

    async def add(self, episode: EpisodeAdd) -> None:
        """Adds new episode to repo.

        Args:
            episode (EpisodeAdd): data for adding episode to repo.

        Returns:
            Episode
        """

        query = """
        INSERT INTO episodes (name, season, number, air_date, show_id)
        VALUES (:name, :season, :number, :air_date, :show_id);
        """

        values = dict(
            name=episode.name,
            season=episode.season,
            number=episode.number,
            air_date=int(episode.air_date.timestamp()),
            show_id=episode.show_id,
        )
        await self._db.execute(query, values=values)

    async def update(self, episode: EpisodeUpdate) -> None:
        """Updates episode in repo.

        Args:
            episode (EpisodeAdd): data for updating episode to repo
        """

        columns_to_update = []
        values = {}

        name = episode.name
        if name is not None:
            columns_to_update.append("name = :name")
            values["name"] = name

        season = episode.season
        if season is not None:
            columns_to_update.append("season = :season")
            values["season"] = season

        number = episode.number
        if number is not None:
            columns_to_update.append("number = :number")
            values["number"] = number

        air_date = episode.air_date
        if air_date is not None:
            columns_to_update.append("air_date = :air_date")
            values["air_date"] = int(air_date.timestamp())

        show_id = episode.show_id
        if show_id is not None:
            columns_to_update.append("show_id = :show_id")
            values["show_id"] = show_id

        query = f"""
        UPDATE episodes
        SET {", ".join(columns_to_update)}
        WHERE id = :id;
        """

        values["id"] = episode.id

        await self._db.execute(query, values=values)

    async def delete(self, episode_id: int) -> None:
        """Deletes episode with id `episode_id` from repo.

        Args:
            episode_id (int)
        """

        query = """
        DELETE FROM episodes
        WHERE id = :id
        """

        values = dict(id=episode_id)
        await self._db.execute(query, values=values)
