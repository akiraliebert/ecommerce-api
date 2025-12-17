import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.application.use_cases.cart.clear_cart import ClearCartUseCase
from app.domain.entities.cart import Cart


@pytest.mark.asyncio
async def test_clear_cart_success():
    user_id = uuid4()
    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=uuid4(), quantity=2)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = cart

    uc = ClearCartUseCase(mock_uow, mock_repo)

    await uc.execute(user_id=user_id)

    assert cart.items == []
    mock_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_clear_cart_not_existing():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = None

    uc = ClearCartUseCase(mock_uow, mock_repo)

    await uc.execute(user_id=uuid4())

    mock_repo.create.assert_not_awaited()
    mock_repo.update.assert_not_awaited()
