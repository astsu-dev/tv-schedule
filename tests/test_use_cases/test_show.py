from unittest import mock

import pytest

from tvsched.application.exceptions.show import (
    ShowNotFoundError,
)
from tvsched.application.models.show import ShowAdd, ShowUpdate
from tvsched.application.use_cases.show.add_show_use_case import AddShowUseCase
from tvsched.application.use_cases.show.delete_show_use_case import DeleteShowUseCase
from tvsched.application.use_cases.show.get_shows_use_case import GetShowsUseCase
from tvsched.application.use_cases.show.update_show_use_case import UpdateShowUseCase
from tvsched.entities.actor import Actor
from tvsched.entities.show import Show
from tvsched.application.use_cases.show.get_show_use_case import GetShowUseCase


@pytest.mark.asyncio
async def test_get_show_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetShowUseCase(repo, logger)

    show_id = 5
    show = Show(
        id=show_id,
        name="Game of Thrones",
        seasons_count=8,
        image_url="url",
        cast=[Actor(id=2, name="Peter", image_url="url")],
    )
    repo.get.return_value = show

    res = await use_case.execute(show_id)

    assert res == show
    repo.get.assert_awaited_once_with(show_id)

    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_get_show_use_case_when_show_not_exists() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetShowUseCase(repo, logger)

    show_id = 6
    repo.get.side_effect = ShowNotFoundError(show_id)

    with pytest.raises(ShowNotFoundError):
        await use_case.execute(show_id)

    repo.get.assert_awaited_once_with(show_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_get_shows_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetShowsUseCase(repo, logger)

    shows = [
        Show(
            id=1,
            name="GOT",
            seasons_count=8,
            image_url="url",
            cast=[Actor(id=1, name="name", image_url="test_url")],
        )
    ]
    repo.get_shows.return_value = shows

    res = await use_case.execute()

    assert res == shows
    repo.get_shows.assert_awaited_once_with(limit=None, offset=None)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_get_shows_use_case_with_limit() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetShowsUseCase(repo, logger)

    limit = 10
    shows = [
        Show(
            id=1,
            name="GOT",
            seasons_count=8,
            image_url="url",
            cast=[Actor(id=1, name="name", image_url="test_url")],
        )
    ]
    repo.get_shows.return_value = shows

    res = await use_case.execute(limit=limit)

    assert res == shows
    repo.get_shows.assert_awaited_once_with(limit=limit, offset=None)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_get_shows_use_case_with_offset() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetShowsUseCase(repo, logger)

    offset = 10
    shows = [
        Show(
            id=1,
            name="GOT",
            seasons_count=8,
            image_url="url",
            cast=[Actor(id=1, name="name", image_url="test_url")],
        )
    ]
    repo.get_shows.return_value = shows

    res = await use_case.execute(offset=offset)

    assert res == shows
    repo.get_shows.assert_awaited_once_with(limit=None, offset=offset)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_show_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddShowUseCase(repo, logger)

    show = ShowAdd(name="show", seasons_count=8, image_url="url")

    await use_case.execute(show)

    repo.add.assert_awaited_once_with(show)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_delete_show_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = DeleteShowUseCase(repo, logger)

    show_id = 5

    await use_case.execute(show_id)

    repo.delete.assert_awaited_once_with(show_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_update_show_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = UpdateShowUseCase(repo, logger)

    show = ShowUpdate(id=5, name="test")

    await use_case.execute(show)

    repo.update.assert_awaited_once_with(show)
    assert logger.info.call_count == 2
