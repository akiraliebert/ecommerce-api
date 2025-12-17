import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime, timezone


from app.application.use_cases.user.authenticate_user import AuthenticateUserUseCase
from app.domain.entities.user import User


@pytest.mark.asyncio
async def test_authenticate_user_success():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = User(
        id=uuid4(),
        email='test@gmail.com',
        hashed_password='hashed',
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )

    mock_password_hasher = Mock()
    mock_password_hasher.verify.return_value = True

    uc = AuthenticateUserUseCase(mock_uow, mock_repo, mock_password_hasher)

    result = await uc.execute(email='test@gmail.com', password='pass')

    assert result.email == 'test@gmail.com'
    mock_repo.get_by_email.assert_awaited_once()
    mock_password_hasher.verify.assert_called_once_with('pass', 'hashed')


@pytest.mark.asyncio
async def test_authenticate_user_not_found():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = None

    mock_password_hasher = Mock()

    uc = AuthenticateUserUseCase(mock_uow, mock_repo, mock_password_hasher)

    with pytest.raises(ValueError, match="Invalid credentials"):
        await uc.execute(email='test@gmail.com', password='pass')

    mock_password_hasher.verify.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_is_inactive():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = User(
        id=uuid4(),
        email='test@gmail.com',
        hashed_password='hashed',
        is_active=False,
        created_at=datetime.now(timezone.utc)
    )

    mock_password_hasher = Mock()

    uc = AuthenticateUserUseCase(mock_uow, mock_repo, mock_password_hasher)

    with pytest.raises(ValueError, match="User is inactive"):
        await uc.execute(email='test@gmail.com', password='pass')

    mock_password_hasher.verify.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = User(
        id=uuid4(),
        email='test@gmail.com',
        hashed_password='hashed',
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )

    mock_password_hasher = Mock()
    mock_password_hasher.verify.return_value = False

    uc = AuthenticateUserUseCase(mock_uow, mock_repo, mock_password_hasher)

    with pytest.raises(ValueError, match="Invalid credentials"):
        await uc.execute(email='test@gmail.com', password='pass')

    mock_password_hasher.verify.assert_called_once_with('pass', 'hashed')
