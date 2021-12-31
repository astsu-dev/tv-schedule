import datetime

from tvsched.adapters.repos.episode.models import EpisodeRecord
from tvsched.entities.episode import Episode


def map_episode_record_to_model(record: EpisodeRecord) -> Episode:
    """Maps db episode record to entity.

    Args:
        record (EpisodeRecord)

    Returns:
        Episode
    """

    return Episode(
        id=record["id"],
        name=record["name"],
        season=record["season"],
        number=record["number"],
        air_date=datetime.datetime.fromtimestamp(record["air_date"]),
        show_id=record["show_id"],
    )
