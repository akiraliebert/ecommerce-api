import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.application.use_cases.cart.get_cart import GetCartUseCase
from app.domain.entities.cart import Cart


@pytest.mark.asyncio
async def test_get_cart_existing():
    user_id = uuid4()
    cart = Cart.create(user_id=user_id)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = cart

    uc = GetCartUseCase(mock_uow, mock_repo)

    result = await uc.execute(user_id=user_id)

    assert result.user_id == user_id
    assert result.items == []
    mock_repo.get_by_user_id.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_cart_creates_if_not_exists():
    user_id = uuid4()

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = None

    uc = GetCartUseCase(mock_uow, mock_repo)

    result = await uc.execute(user_id=user_id)

    assert result.user_id == user_id
    mock_repo.create.assert_awaited_once()
