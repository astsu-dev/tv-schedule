from tvsched.application.models.show import ShowAdd


class ShowNotFoundError(Exception):
    """Will be raised if show not found in repo"""

    def __init__(self, show_id: int) -> None:
        self._show_id = show_id

    @property
    def show_id(self) -> int:
        return self._show_id


class ShowAlreadyExistsError(Exception):
    """Will be raised when trying to add already existed show to repo"""

    def __init__(self, show: ShowAdd) -> None:
        self._show = show

    @property
    def show(self) -> ShowAdd:
        return self._show
