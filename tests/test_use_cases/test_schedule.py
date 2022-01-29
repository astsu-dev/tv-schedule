import datetime
import uuid
from unittest import mock

import pytest

from tvsched.application.exceptions.schedule import (
    EpisodeAlreadyMarkedAsWatchedError,
    EpisodeOrScheduleNotFoundError,
    ShowOrScheduleNotFoundError,
    ShowAlreadyExistsInScheduleError,
)
from tvsched.application.models.schedule import EpisodeInSchedule, ShowInSchedule
from tvsched.application.use_cases.schedule.get_first_unwatched_episodes_use_case import (
    GetFirstUnwatchedEpisodesFromScheduleUseCase,
)
from tvsched.application.use_cases.schedule.mark_episode_as_unwatched_use_case import (
    MarkEpisodeAsUnwatchedUseCase,
)
from tvsched.application.use_cases.schedule.mark_episode_as_watched_use_case import (
    MarkEpisodeAsWatchedUseCase,
)
from tvsched.application.use_cases.schedule.get_shows_from_schedule_use_case import (
    GetShowsFromScheduleUseCase,
)
from tvsched.application.use_cases.schedule.add_show_to_schedule_use_case import (
    AddShowToScheduleUseCase,
)
from tvsched.application.use_cases.schedule.get_suggested_shows_use_case import (
    GetSuggestedShowsUseCase,
)
from tvsched.application.use_cases.schedule.delete_show_from_schedule_use_case import (
    DeleteShowFromScheduleUseCase,
)
from tvsched.entities.actor import Actor
from tvsched.entities.episode import Episode
from tvsched.entities.show import Show


@pytest.mark.asyncio
async def test_get_shows_from_schedule_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetShowsFromScheduleUseCase(repo, logger)

    user_id = uuid.uuid4()
    shows = [
        Show(
            id=1,
            name="GOT",
            seasons_count=8,
            image_url="url",
            cast=[Actor(id=1, name="name", image_url="test_url")],
        )
    ]
    repo.get_shows_from_schedule.return_value = shows

    res = await use_case.execute(user_id)

    assert res == shows
    repo.get_shows_from_schedule.assert_awaited_once_with(user_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_show_to_schedule_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddShowToScheduleUseCase(repo, logger)

    show_add = ShowInSchedule(show_id=5, user_id=uuid.uuid4())

    await use_case.execute(show_add)
    repo.add_to_schedule.assert_awaited_once_with(show_add)

    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_show_to_schedule_use_case_when_show_or_schedule_not_exists() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddShowToScheduleUseCase(repo, logger)

    show_id = 5
    show_in_schedule = ShowInSchedule(show_id=show_id, user_id=uuid.uuid4())
    repo.add_to_schedule.side_effect = ShowOrScheduleNotFoundError(show_id)

    with pytest.raises(ShowOrScheduleNotFoundError):
        await use_case.execute(show_in_schedule)

    repo.add_to_schedule.assert_awaited_once_with(show_in_schedule)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_show_to_schedule_use_case_when_show_already_in_schedule() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddShowToScheduleUseCase(repo, logger)

    show_id = 5
    show_in_schedule = ShowInSchedule(show_id=show_id, user_id=uuid.uuid4())
    repo.add_to_schedule.side_effect = ShowAlreadyExistsInScheduleError(
        show_in_schedule
    )

    with pytest.raises(ShowAlreadyExistsInScheduleError):
        await use_case.execute(show_in_schedule)

    repo.add_to_schedule.assert_awaited_once_with(show_in_schedule)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_delete_show_from_schedule_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = DeleteShowFromScheduleUseCase(repo, logger)

    show_in_schedule = ShowInSchedule(show_id=5, user_id=uuid.uuid4())

    await use_case.execute(show_in_schedule)
    repo.delete_from_schedule.assert_awaited_once_with(show_in_schedule)

    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_get_suggested_shows_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetSuggestedShowsUseCase(repo, logger)

    user_id = uuid.uuid4()
    shows = [
        Show(
            id=5,
            name="Game of Thrones",
            seasons_count=8,
            image_url="url",
            cast=[Actor(id=2, name="Peter", image_url="url")],
        )
    ]
    repo.get_suggested_shows.return_value = shows

    res = await use_case.execute(user_id)

    assert res == shows
    repo.get_suggested_shows.assert_awaited_once_with(user_id)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_mark_episode_as_watched_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = MarkEpisodeAsWatchedUseCase(repo, logger)

    episode_in_schedule = EpisodeInSchedule(episode_id=5, user_id=uuid.uuid4())

    await use_case.execute(episode_in_schedule)

    repo.mark_episode_as_watched.assert_awaited_once_with(episode_in_schedule)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_mark_episode_as_watched_use_case_when_episode_or_schedule_does_not_exists() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = MarkEpisodeAsWatchedUseCase(repo, logger)

    episode_in_schedule = EpisodeInSchedule(episode_id=5, user_id=uuid.uuid4())
    repo.mark_episode_as_watched.side_effect = EpisodeOrScheduleNotFoundError(
        episode_in_schedule
    )

    with pytest.raises(EpisodeOrScheduleNotFoundError):
        await use_case.execute(episode_in_schedule)

    repo.mark_episode_as_watched.assert_awaited_once_with(episode_in_schedule)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_mark_episode_as_watched_use_case_when_episode_already_marked() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = MarkEpisodeAsWatchedUseCase(repo, logger)

    episode_in_schedule = EpisodeInSchedule(episode_id=5, user_id=uuid.uuid4())
    repo.mark_episode_as_watched.side_effect = EpisodeAlreadyMarkedAsWatchedError(
        episode_in_schedule
    )

    with pytest.raises(EpisodeAlreadyMarkedAsWatchedError):
        await use_case.execute(episode_in_schedule)

    repo.mark_episode_as_watched.assert_awaited_once_with(episode_in_schedule)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_mark_episode_as_unwatched_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = MarkEpisodeAsUnwatchedUseCase(repo, logger)

    episode_in_schedule = EpisodeInSchedule(episode_id=5, user_id=uuid.uuid4())

    await use_case.execute(episode_in_schedule)

    repo.mark_episode_as_unwatched.assert_awaited_once_with(episode_in_schedule)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_get_first_unwatched_episodes_from_schedule_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = GetFirstUnwatchedEpisodesFromScheduleUseCase(repo, logger)

    user_id = uuid.uuid4()
    episodes = [
        Episode(
            id=1,
            name="test",
            season=5,
            number=2,
            air_date=datetime.datetime.now(),
            show_id=5,
        )
    ]
    repo.get_first_unwatched_episodes_from_schedule.return_value = episodes

    res = await use_case.execute(user_id)

    assert res == episodes
    repo.get_first_unwatched_episodes_from_schedule.assert_awaited_once_with(user_id)
    assert logger.info.call_count == 2
