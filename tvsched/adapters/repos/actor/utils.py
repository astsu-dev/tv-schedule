from tvsched.adapters.repos.actor.models import ActorRecord
from tvsched.entities.actor import Actor


def map_actor_record_to_model(record: ActorRecord) -> Actor:
    """Maps db actor record to entity.

    Args:
        record (ActorRecord)

    Returns:
        Actor
    """

    return Actor(id=record["id"], name=record["name"], image_url=record["image_url"])
