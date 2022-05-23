import datetime
from unittest import mock
import uuid

import pytest
from tvsched.application.exceptions.auth import UserAlreadyExistsError, UserNotFoundError

from tvsched.application.models.auth import (
    UserAdd,
    UserInRepo,
    UserLogIn,
    UserWithRoleAdd,
    UserInRepoAdd,
)
from tvsched.application.use_cases.auth.add_user_use_case import AddUserUseCase
from tvsched.application.use_cases.auth.add_user_with_role_use_case import (
    AddUserWithRoleUseCase,
)
from tvsched.application.use_cases.auth.log_in_user_use_case import LogInUserUseCase
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
        UserInRepoAdd(username=username, password_hash=password_hash, role=role)
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
        UserInRepoAdd(username=username, password_hash=password_hash, role=role)
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
        UserInRepoAdd(username=username, password_hash=password_hash, role=role)
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
        UserInRepoAdd(username=username, password_hash=password_hash, role=role)
    )
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_log_in_user_use_case() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = LogInUserUseCase(
        repo,
        logger,
        jwt_secret="secret",
        jwt_expires_in=datetime.timedelta(seconds=3600),
        jwt_algorithm="HS256",
    )

    username = "user"
    password = "password"
    password_hash = "$2b$12$7H.90bastmQ1Lqo0sVLxguLfmdW6pqLTT7Ky8IzPi/B/h.BRLTKgm"
    role = Role.USER
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoiYjZlZDc0N2YtZDNkOS00OTYyLWEwOTAtMjllMjYyM2EzZjYzIiwicm9sZSI6IlVTRVIifSwic3ViIjoiYjZlZDc0N2YtZDNkOS00OTYyLWEwOTAtMjllMjYyM2EzZjYzIiwiaWF0IjoxNjQzNTI2NzEzLCJleHAiOjE2NDM1MzAzMTN9.bLUDVQeJKSH4W75fVZ5VrbjB_OGo7HOpBB-cLzGbbbc"
    user_log_in = UserLogIn(username=username, password=password)
    repo.get_user_by_username.return_value = UserInRepo(
        id=uuid.UUID("b6ed747f-d3d9-4962-a090-29e2623a3f63"),
        username=username,
        password_hash=password_hash,
        role=role,
    )

    with mock.patch(
        "tvsched.application.use_cases.auth.log_in_user_use_case.create_access_token_for_user"
    ) as create_access_token_for_user:
        create_access_token_for_user.return_value = token

        res = await use_case.execute(user_log_in)

    assert res == token
    repo.get_user_by_username.assert_awaited_once_with(username)
    assert logger.info.call_count == 2


@pytest.mark.asyncio
async def test_log_in_user_use_case_when_user_not_exist() -> None:
    repo = mock.AsyncMock()
    logger = mock.Mock()
    use_case = LogInUserUseCase(
        repo,
        logger,
        jwt_secret="secret",
        jwt_expires_in=datetime.timedelta(seconds=3600),
        jwt_algorithm="HS256",
    )

    username = "user"
    password = "password"
    password_hash = "$2b$12$7H.90bastmQ1Lqo0sVLxguLfmdW6pqLTT7Ky8IzPi/B/h.BRLTKgm"
    role = Role.USER
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoiYjZlZDc0N2YtZDNkOS00OTYyLWEwOTAtMjllMjYyM2EzZjYzIiwicm9sZSI6IlVTRVIifSwic3ViIjoiYjZlZDc0N2YtZDNkOS00OTYyLWEwOTAtMjllMjYyM2EzZjYzIiwiaWF0IjoxNjQzNTI2NzEzLCJleHAiOjE2NDM1MzAzMTN9.bLUDVQeJKSH4W75fVZ5VrbjB_OGo7HOpBB-cLzGbbbc"
    user_log_in = UserLogIn(username=username, password=password)
    repo.get_user_by_username.side_effect = UserNotFoundError(username)

    with mock.patch(
        "tvsched.application.use_cases.auth.log_in_user_use_case.create_access_token_for_user"
    ) as create_access_token_for_user:
        create_access_token_for_user.return_value = token

        with pytest.raises(UserNotFoundError):
            await use_case.execute(user_log_in)

    repo.get_user_by_username.assert_awaited_once_with(username)
    assert logger.info.call_count == 2
