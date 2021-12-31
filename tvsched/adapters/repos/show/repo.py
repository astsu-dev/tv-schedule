from typing import Optional
import typing
import uuid

from databases.core import Connection

from tvsched.adapters.repos.show.models import ShowRecord
from tvsched.adapters.repos.show.utils import (
    group_show_records,
    map_show_records_to_model,
)
from tvsched.application.exceptions.show import ShowNotFoundError
from tvsched.application.models.show import ShowAdd, ShowUpdate
from tvsched.entities.show import Show


class ShowRepo:
    def __init__(self, db: Connection) -> None:
        self._db = db

    async def get(self, show_id: int) -> Show:
        """Returns show from repo by `show_id`.

        Args:
            show_id (show)

        Raises:
            ShowNotFoundError: will be raised if show with id `show_id` not in repo

        Returns:
            Show
        """

        query = """
        SELECT s.*, a.id as actor_id, a.name as actor_name,
        a.image_url as actor_image_url
        FROM shows s
        JOIN actors_to_shows ats ON ats.show_id = s.id
        JOIN actors a ON ats.actor_id = a.id
        WHERE s.id = :show_id;
        """

        values = dict(show_id=show_id)
        records = await self._db.fetch_all(query, values=values)
        records = typing.cast(list[ShowRecord], records)

        if not records:
            raise ShowNotFoundError(show_id=show_id)

        show = map_show_records_to_model(records)

        return show

    async def get_shows(
        self, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> list[Show]:
        """Returns list of shows from repo by.

        Args:
            limit (Optional[int]): max number of shows. If None all shows will be returned
            offset (Optional[int])

        Returns:
            list[Show]
        """

        query = """
        SELECT s.*, a.id as actor_id, a.name as actor_name,
        a.image_url as actor_image_url
        FROM shows s
        JOIN actors_to_shows ats ON ats.show_id = s.id
        JOIN actors a ON ats.actor_id = a.id
        LIMIT :limit
        OFFSET :offset;
        """

        values = dict(limit=limit, offset=offset)
        records = await self._db.fetch_all(query, values)
        records = typing.cast(list[ShowRecord], records)
        grouped_records = group_show_records(records)
        res = [map_show_records_to_model(rs) for rs in grouped_records]

        return res

    async def add(self, show: ShowAdd) -> None:
        """Adds show to repo.

        Args:
            show (ShowAdd): data for adding show to repo

        Raises:
            ShowAlreadyExistsError: will be raised if show with id `showh.id`
                already exists in repo
        """

        query = """
        INSERT INTO shows (name, seasons_count, image_url)
        VALUES (:name, :seasons_count, :image_url);
        """

        values = dict(
            name=show.name, seasons_count=show.seasons_count, image_url=show.image_url
        )
        await self._db.execute(query, values=values)

    async def delete(self, show_id: int) -> None:
        """Deletes show from repo by `show_id`.

        Args:
            show_id (show)

        Returns:
            Show
        """

        query = """
        DELETE FROM shows WHERE id = :show_id;
        """

        values = dict(show_id=show_id)
        await self._db.execute(query, values=values)

    async def update(self, show: ShowUpdate) -> None:
        """Updates show in repo.

        Args:
            show (ShowAdd): data for updating show to repo
        """

        columns_to_update = []
        values = {}

        name = show.name
        if name is not None:
            columns_to_update.append("name = :name")
            values["name"] = name

        seasons_count = show.seasons_count
        if seasons_count is not None:
            columns_to_update.append("seasons_count = :seasons_count")
            values["seasons_count"] = seasons_count

        image_url = show.image_url
        if image_url is not None:
            columns_to_update.append("image_url = :image_url")
            values["image_url"] = image_url

        query = f"""
        UPDATE shows
        SET {", ".join(columns_to_update)}
        WHERE id = :id;
        """

        values["id"] = show.id

        await self._db.execute(query, values=values)

    async def get_shows_from_schedule(
        self,
        user_id: uuid.UUID,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Show]:
        """Returns list of shows from user schedule.

        Args:
            user_id (uuid.UUID): user schedule user user_id

        Returns:
            list[Show]
        """

        query = """
        SELECT s.*, a.id as actor_id, a.name as actor_name,
        a.image_url as actor_image_url
        FROM shows s
        JOIN actors_to_shows ats ON ats.show_id = s.id
        JOIN actors a ON ats.actor_id = a.id
        JOIN shows_to_schedules sts ON sts.show_id = s.id
        WHERE sts.user_id = :user_id
        LIMIT :limit
        OFFSET :offset;
        """

        values = dict(user_id=user_id, limit=limit, offset=offset)
        records = await self._db.fetch_all(query, values)
        records = typing.cast(list[ShowRecord], records)
        grouped_records = group_show_records(records)
        shows = [map_show_records_to_model(rs) for rs in grouped_records]

        return shows
