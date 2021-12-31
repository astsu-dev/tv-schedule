from unittest import mock

import pytest

from tvsched.application.exceptions.actor import (
    ActorAlreadyInShowCastError,
    ActorNotFoundError,
    ActorOrShowNotFoundError,
)
from tvsched.application.models.actor import ActorAdd, ActorInShowCast, ActorUpdate
from tvsched.application.use_cases.actor.add_actor_to_show_cast_use_case import (
    AddActorToShowCastUseCase,
)
from tvsched.application.use_cases.actor.add_actor_use_case import AddActorUseCase
from tvsched.application.use_cases.actor.delete_actor_from_show_cast_use_case import (
    DeleteActorFromShowCastUseCase,
)
from tvsched.application.use_cases.actor.delete_actor_use_case import DeleteActorUseCase
from tvsched.application.use_cases.actor.get_actor_use_case import GetActorUseCase
from tvsched.application.use_cases.actor.update_actor_use_case import UpdateActorUseCase
from tvsched.entities.actor import Actor


@pytest.mark.asyncio
async def test_get_actor_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetActorUseCase(repo, logger)

    expected = Actor(id=1, name="James", image_url="url")
    repo.get.return_value = expected
    actor_id = 1

    actor = await use_case.execute(actor_id)

    assert actor == expected
    repo.get.assert_awaited_once_with(actor_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_get_actor_use_case_when_actor_not_exists() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetActorUseCase(repo, logger)

    actor_id = 1
    repo.get.side_effect = ActorNotFoundError(actor_id)

    with pytest.raises(ActorNotFoundError):
        await use_case.execute(actor_id)

    repo.get.assert_awaited_once_with(actor_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_actor_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddActorUseCase(repo, logger)

    actor = ActorAdd(name="James", image_url="url")

    await use_case.execute(actor)

    repo.add.assert_awaited_once_with(actor)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_delete_actor_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = DeleteActorUseCase(repo, logger)

    actor_id = 1

    await use_case.execute(actor_id)

    repo.delete.assert_awaited_once_with(actor_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_update_actor_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = UpdateActorUseCase(repo, logger)

    actor = ActorUpdate(id=1, name="James", image_url="url")

    await use_case.execute(actor)

    repo.update.assert_awaited_once_with(actor)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_actor_to_show_cast_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddActorToShowCastUseCase(repo, logger)

    actor_in_cast = ActorInShowCast(show_id=5, actor_id=1)

    await use_case.execute(actor_in_cast)

    repo.add_actor_to_show_cast.assert_awaited_once_with(actor_in_cast)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_actor_to_show_cast_use_case_when_actor_or_show_not_exists() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddActorToShowCastUseCase(repo, logger)

    show_id = 5
    actor_in_cast = ActorInShowCast(show_id=show_id, actor_id=1)
    repo.add_actor_to_show_cast.side_effect = ActorOrShowNotFoundError(actor_in_cast)

    with pytest.raises(ActorOrShowNotFoundError):
        await use_case.execute(actor_in_cast)

    repo.add_actor_to_show_cast.assert_awaited_once_with(actor_in_cast)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_actor_to_show_cast_use_case_when_actor_already_exists_in_show_cast() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddActorToShowCastUseCase(repo, logger)

    show_id = 5
    actor_in_cast = ActorInShowCast(show_id=show_id, actor_id=1)
    repo.add_actor_to_show_cast.side_effect = ActorAlreadyInShowCastError(actor_in_cast)

    with pytest.raises(ActorAlreadyInShowCastError):
        await use_case.execute(actor_in_cast)

    repo.add_actor_to_show_cast.assert_awaited_once_with(actor_in_cast)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_delete_actor_from_show_cast_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = DeleteActorFromShowCastUseCase(repo, logger)

    actor_in_cast = ActorInShowCast(show_id=5, actor_id=1)

    await use_case.execute(actor_in_cast)

    repo.delete_actor_from_show_cast.assert_awaited_once_with(actor_in_cast)
    assert logger.info.call_count == 2
