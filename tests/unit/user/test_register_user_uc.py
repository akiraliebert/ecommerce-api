import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime, timezone


from app.application.use_cases.user.register_user import RegisterUserUseCase
from app.application.dto.user_dto import CreateUserDTO
from app.domain.entities.user import User


@pytest.mark.asyncio
async def test_register_user_success():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow


    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = None

    mock_password_hasher = Mock()
    mock_password_hasher.hash.return_value = 'hashed_pass'

    uc = RegisterUserUseCase(mock_uow, mock_repo, mock_password_hasher)

    result = await uc.execute(CreateUserDTO(email='test@gmail.com', password='pass'))

    assert result.email == 'test@gmail.com'
    mock_password_hasher.hash.assert_called_once_with('pass')
    mock_repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_existing_email():
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

    uc = RegisterUserUseCase(mock_uow, mock_repo, mock_password_hasher)

    with pytest.raises(ValueError, match="User with this email already exists"):
        await uc.execute(
            CreateUserDTO(email='test@gmail.com', password='pass')
        )

    mock_repo.create.assert_not_called()
