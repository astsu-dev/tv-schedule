from unittest import mock

import pytest
from tvsched.application.exceptions.auth import UserAlreadyExistsError

from tvsched.application.models.auth import UserAdd, UserWithRoleAdd, UserInRepo
from tvsched.application.use_cases.auth.add_user_use_case import AddUserUseCase
from tvsched.application.use_cases.auth.add_user_with_role_use_case import (
    AddUserWithRoleUseCase,
)
from tvsched.entities.auth import Role


@pytest.mark.asyncio
async def test_add_user_with_role_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddUserWithRoleUseCase(repo, logger)

    username = "user"
    password_hash = "hash"
    role = Role.USER
    user_with_role = UserWithRoleAdd(username=username, password="password", role=role)

    with mock.patch(
        "tvsched.application.use_cases.auth.add_user_with_role_use_case.hash_password"
    ) as hash_password:
        hash_password.return_value = password_hash

        await use_case.execute(user_with_role)

    repo.add_user.assert_awaited_once_with(
        UserInRepo(username=username, password_hash=password_hash, role=role)
    )
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_user_with_role_use_case_when_user_already_exists() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddUserWithRoleUseCase(repo, logger)

    username = "user"
    password_hash = "hash"
    role = Role.USER
    user_with_role = UserWithRoleAdd(username=username, password="password", role=role)

    repo.add_user.side_effect = UserAlreadyExistsError(username)

    with mock.patch(
        "tvsched.application.use_cases.auth.add_user_with_role_use_case.hash_password"
    ) as hash_password:
        hash_password.return_value = password_hash

        with pytest.raises(UserAlreadyExistsError):
            await use_case.execute(user_with_role)

    repo.add_user.assert_awaited_once_with(
        UserInRepo(username=username, password_hash=password_hash, role=role)
    )
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_user_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddUserUseCase(repo, logger)

    username = "user"
    password_hash = "hash"
    role = Role.USER
    user_add = UserAdd(username=username, password="password")

    with mock.patch(
        "tvsched.application.use_cases.auth.add_user_with_role_use_case.hash_password"
    ) as hash_password:
        hash_password.return_value = password_hash

        await use_case.execute(user_add)

    repo.add_user.assert_awaited_once_with(
        UserInRepo(username=username, password_hash=password_hash, role=role)
    )
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_add_user_use_case_when_user_already_exists() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = AddUserUseCase(repo, logger)

    username = "user"
    password_hash = "hash"
    role = Role.USER
    user_add = UserAdd(username=username, password="password")

    repo.add_user.side_effect = UserAlreadyExistsError(username)

    with mock.patch(
        "tvsched.application.use_cases.auth.add_user_with_role_use_case.hash_password"
    ) as hash_password:
        hash_password.return_value = password_hash

        with pytest.raises(UserAlreadyExistsError):
            await use_case.execute(user_add)

    repo.add_user.assert_awaited_once_with(
        UserInRepo(username=username, password_hash=password_hash, role=role)
    )
    assert logger.info.call_count == 2
