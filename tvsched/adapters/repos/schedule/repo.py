import typing
import uuid
from typing import Optional
import asyncpg

from databases.core import Connection

from tvsched.adapters.repos.show.models import ShowRecord
from tvsched.adapters.repos.show.utils import (
    group_show_records,
    map_show_records_to_model,
)
from tvsched.application.exceptions.schedule import (
    EpisodeAlreadyMarkedAsWatchedError,
    EpisodeOrScheduleNotFoundError,
    ShowOrScheduleNotFoundError,
    ShowAlreadyExistsInScheduleError,
)
from tvsched.application.models.schedule import EpisodeInSchedule, ShowInSchedule
from tvsched.entities.episode import Episode
from tvsched.entities.show import Show


class ScheduleRepo:
    def __init__(self, db: Connection) -> None:
        self._db = db

    async def get_shows_from_schedule(
        self,
        user_id: uuid.UUID,
        limit: Optional[int] = None,
        offset: typing.Optional[int] = None,
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

    async def add_show_to_schedule(self, show_in_schedule: ShowInSchedule) -> None:
        """Adds show with id `show_in_schedule.show_id` to user schedule
        with id `show_in_schedule.user_id`.

        Args:
            show_in_schedule (ShowInSchedule): data for adding show to schedule
        """

        query = """
        INSERT INTO shows_to_schedules (user_id, show_id)
        VALUES (:user_id, :show_id);
        """

        values = dict(
            user_id=show_in_schedule.user_id, show_id=show_in_schedule.show_id
        )
        try:
            await self._db.execute(query, values)
        except asyncpg.exceptions.UniqueViolationError:
            raise ShowAlreadyExistsInScheduleError(show_in_schedule)
        except asyncpg.exceptions.ForeignKeyViolationError:
            raise ShowOrScheduleNotFoundError(show_in_schedule)

    async def delete_show_from_schedule(self, show_in_schedule: ShowInSchedule) -> None:
        """Deletes show with id `show_in_schedule.show_id` from user schedule
        with id `show_in_schedule.user_id`.

        Args:
            show_in_schedule (ShowInSchedule): data for deleting show to schedule
        """

        query = """
        DELETE FROM shows_to_schedules
        WHERE user_id = :user_id AND show_id = :show_id;
        """

        values = dict(
            user_id=show_in_schedule.user_id, show_id=show_in_schedule.show_id
        )
        await self._db.execute(query, values)

    async def get_suggested_shows(self, user_id: uuid.UUID) -> list[Show]:
        """Returns list of suggested shows for user with id `user_id`.

        Args:
            user_id (uuid.UUID)

        Returns:
            list[Show]
        """

        query = """
        SELECT DISTINCT s.*, a.id AS actor_id, a.name AS actor_name, a.image_url AS actor_image_url
        FROM shows s
        JOIN actors_to_shows ats ON s.id = ats.show_id
        JOIN actors a ON a.id = ats.actor_id
        JOIN (SELECT s.*, a.id AS actor_id, a.name AS actor_name, a.image_url AS actor_image_url
            FROM shows s
            JOIN actors_to_shows ats ON s.id = ats.show_id
            JOIN actors a ON a.id = ats.actor_id
            WHERE a.id IN (
                SELECT DISTINCT a2.id AS actor_id
                FROM shows s2
                JOIN shows_to_schedules sts ON sts.show_id = s2.id
                JOIN users u ON u.id = sts.user_id
                JOIN actors_to_shows ats2 ON s2.id = ats2.show_id
                JOIN actors a2 ON a2.id = ats2.actor_id
                WHERE u.id = :user_id
            )
        ) res ON res.id = s.id;
        """

        values = dict(user_id=user_id)
        records = await self._db.fetch_all(query, values)
        records = typing.cast(list[ShowRecord], records)
        grouped_records = group_show_records(records)
        shows = [map_show_records_to_model(rs) for rs in grouped_records]

        return shows

    async def mark_episode_as_watched(
        self, episode_in_schedule: EpisodeInSchedule
    ) -> None:
        """Marks episode with `episode_id` as watched in repo.

        Args:
            episode_in_schedule (EpisodeInSchedule): data for marking episode
                as watched in schedule

        Raises:
            EpisodeOrScheduleNotFoundError: will be raised if episode or schedule does not exists
            EpisodeAlreadyExistsInScheduleError: will be raised if episode already marked as watched in schedule
        """

        query = """
        INSERT INTO watched_episodes (user_id, episode_id)
        VALUES (:user_id, :episode_id);
        """

        values = dict(
            user_id=episode_in_schedule.user_id,
            episode_id=episode_in_schedule.episode_id,
        )

        try:
            await self._db.execute(query, values)
        except asyncpg.exceptions.ForeignKeyViolationError:
            raise EpisodeOrScheduleNotFoundError(episode_in_schedule)
        except asyncpg.exceptions.UniqueViolationError:
            raise EpisodeAlreadyMarkedAsWatchedError(episode_in_schedule)

    async def mark_episode_as_unwatched(
        self, episode_in_schedule: EpisodeInSchedule
    ) -> None:
        """Marks episode with `episode_id` as unwatched in repo.

        Args:
            episode_in_schedule (EpisodeInSchedule): data for marking episode
                as watched in schedule
        """

        query = """
        DELETE FROM watched_episodes
        WHERE user_id = :user_id AND episode_id = :episode_id;
        """

        values = dict(
            user_id=episode_in_schedule.user_id,
            episode_id=episode_in_schedule.episode_id,
        )

        await self._db.execute(query, values)

