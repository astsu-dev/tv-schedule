import datetime
from unittest import mock

import pytest

from tvsched.application.exceptions.episode import EpisodeNotFoundError
from tvsched.application.exceptions.show import ShowNotFoundError
from tvsched.application.models.episode import EpisodeAdd, EpisodeUpdate
from tvsched.application.use_cases.episode.add_episode_use_case import AddEpisodeUseCase
from tvsched.application.use_cases.episode.delete_episode_use_case import (
    DeleteEpisodeUseCase,
)
from tvsched.application.use_cases.episode.get_episode_use_case import GetEpisodeUseCase
from tvsched.application.use_cases.episode.get_episodes_use_case import (
    GetEpisodesFromShowUseCase,
)
from tvsched.application.use_cases.episode.update_episode_use_case import (
    UpdateEpisodeUseCase,
)
from tvsched.entities.episode import Episode


@pytest.mark.asyncio
async def test_get_episode_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetEpisodeUseCase(repo, logger)

    episode_id = 1
    expected = Episode(
        id=episode_id,
        name="name",
        season=5,
        number=3,
        air_date=datetime.datetime.now(),
        show_id=5,
    )
    repo.get.return_value = expected

    episode = await use_case.execute(episode_id)

    assert episode == expected
    repo.get.assert_awaited_once_with(episode_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_get_episode_use_case_when_episode_not_exists() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetEpisodeUseCase(repo, logger)

    episode_id = 1
    repo.get.side_effect = EpisodeNotFoundError(episode_id)

    with pytest.raises(EpisodeNotFoundError):
        await use_case.execute(episode_id)

    repo.get.assert_awaited_once_with(episode_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_episode_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddEpisodeUseCase(repo, logger)

    episode = EpisodeAdd(
        name="name", season=5, number=3, air_date=datetime.datetime.now(), show_id=5
    )

    await use_case.execute(episode)

    repo.add.assert_awaited_once_with(episode)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_delete_episode_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = DeleteEpisodeUseCase(repo, logger)

    episode_id = 5

    await use_case.execute(episode_id)

    repo.delete.assert_awaited_once_with(episode_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_update_episode_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = UpdateEpisodeUseCase(repo, logger)

    episode = EpisodeUpdate(
        id=1,
        name="name",
        season=5,
        number=3,
        air_date=datetime.datetime.now(),
        show_id=5,
    )

    await use_case.execute(episode)

    repo.update.assert_awaited_once_with(episode)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_get_episodes_from_show_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetEpisodesFromShowUseCase(repo, logger)

    show_id = 5
    episodes = [
        Episode(
            id=1,
            name="test",
            season=5,
            number=2,
            air_date=datetime.datetime.now(),
            show_id=show_id,
        )
    ]
    repo.get_episodes_from_show.return_value = episodes

    res = await use_case.execute(show_id)

    assert res == episodes
    repo.get_episodes_from_show.assert_awaited_once_with(show_id)
    assert logger.info.call_count == 2
