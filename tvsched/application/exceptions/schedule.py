from tvsched.application.models.schedule import EpisodeInSchedule, ShowInSchedule


class ShowAlreadyExistsInScheduleError(Exception):
    """Will be raised when trying to add already existed in schedule show to schedule"""

    def __init__(self, show_in_schedule: ShowInSchedule) -> None:
        self._show_in_schedule = show_in_schedule

    @property
    def show_in_schedule(self) -> ShowInSchedule:
        return self._show_in_schedule


class ShowOrScheduleNotFoundError(Exception):
    """Will be raised when trying to add not existed show to schedule
    or show to not existed schedule
    """

    def __init__(self, show_in_schedule: ShowInSchedule) -> None:
        self._show_in_schedule = show_in_schedule

    @property
    def show_in_schedule(self) -> ShowInSchedule:
        return self._show_in_schedule


class EpisodeOrScheduleNotFoundError(Exception):
    """Will be raised when trying to add not existed episode to schedule
    or episode to not existed schedule
    """

    def __init__(self, episode_in_schedule: EpisodeInSchedule) -> None:
        self._episode_in_schedule = episode_in_schedule

    @property
    def episode_in_schedule(self) -> EpisodeInSchedule:
        return self._episode_in_schedule


class EpisodeAlreadyMarkedAsWatchedError(Exception):
    """Will be raised when trying to mark as watched
    already marked episode in schedule.
    """

    def __init__(self, episode_in_schedule: EpisodeInSchedule) -> None:
        self._episode_in_schedule = episode_in_schedule

    @property
    def episode_in_schedule(self) -> EpisodeInSchedule:
        return self._episode_in_schedule
