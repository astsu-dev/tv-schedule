import typing

import asyncpg
from databases.core import Connection

from tvsched.adapters.repos.actor.models import ActorRecord
from tvsched.adapters.repos.actor.utils import (
    map_actor_record_to_model,
)
from tvsched.application.exceptions.actor import (
    ActorAlreadyInShowCastError,
    ActorNotFoundError,
    ActorOrShowNotFoundError,
)
from tvsched.application.models.actor import ActorAdd, ActorInShowCast, ActorUpdate
from tvsched.entities.actor import Actor


class ActorRepo:
    def __init__(self, db: Connection) -> None:
        self._db = db

    async def get(self, actor_id: int) -> Actor:
        """Returns actor from repo by `actor_id`.

        Args:
            actor_id (int)

        Raises:
            ActorNotFoundError: will be raised if actor with id `actor_id` not in repo

        Returns:
            Actor
        """

        query = """
        SELECT * FROM actors
        WHERE id = :id;
        """

        values = dict(id=actor_id)
        record = await self._db.fetch_one(query, values=values)

        if record is None:
            raise ActorNotFoundError(actor_id=actor_id)

        actor_record = typing.cast(ActorRecord, record)
        actor = map_actor_record_to_model(actor_record)

        return actor

    async def add(self, actor: ActorAdd) -> None:
        """Adds new actor to repo.

        Args:
            actor (ActorAdd): data for adding actor to repo.

        Returns:
            Actor
        """

        query = """
        INSERT INTO actors (name, image_url)
        VALUES (:name, :image_url);
        """

        values = dict(
            name=actor.name,
            image_url=actor.image_url,
        )
        await self._db.execute(query, values=values)

    async def update(self, actor: ActorUpdate) -> None:
        """Updates actor in repo.

        Args:
            actor (ActorAdd): data for updating actor in repo
        """

        columns_to_update = []
        values = {}

        name = actor.name
        if name is not None:
            columns_to_update.append("name = :name")
            values["name"] = name

        image_url = actor.image_url
        if image_url is not None:
            columns_to_update.append("image_url = :image_url")
            values["image_url"] = image_url

        query = f"""
        UPDATE actors
        SET {", ".join(columns_to_update)}
        WHERE id = :id;
        """

        values["id"] = actor.id

        await self._db.execute(query, values=values)

    async def delete(self, actor_id: int) -> None:
        """Deletes actor with id `actor_id` from repo.

        Args:
            actor_id (int)
        """

        query = """
        DELETE FROM actors
        WHERE id = :id;
        """

        values = dict(id=actor_id)
        await self._db.execute(query, values=values)

    async def add_actor_to_show_cast(self, actor_in_cast: ActorInShowCast) -> None:
        """Adds actor with id `actor_in_cast.actor_id` to show cast with id `actor_in_cast.show_id`.

        Args:
            actor_in_cast (ActorInShowCast): data for adding actor to show cast
        """

        query = """
        INSERT INTO actors_to_shows (show_id, actor_id)
        VALUES (:show_id, :actor_id);
        """

        values = dict(show_id=actor_in_cast.show_id, actor_id=actor_in_cast.actor_id)

        try:
            await self._db.execute(query, values=values)
        except asyncpg.exceptions.ForeignKeyViolationError:
            raise ActorOrShowNotFoundError(actor_in_cast)
        except asyncpg.exceptions.UniqueViolationError:
            raise ActorAlreadyInShowCastError(actor_in_cast)

    async def delete_actor_from_show_cast(self, actor_in_cast: ActorInShowCast) -> None:
        """Deletes actor with id `actor_in_cast.actor_id` from show cast with id `actor_in_cast.show_id`.

        Args:
            actor_in_cast (ActorInShowCast): data for deleting actor from show cast
        """

        query = """
        DELETE FROM actors_to_shows
        WHERE show_id = :show_id AND actor_id = :actor_id;
        """

        values = dict(show_id=actor_in_cast.show_id, actor_id=actor_in_cast.actor_id)
        await self._db.execute(query, values=values)
