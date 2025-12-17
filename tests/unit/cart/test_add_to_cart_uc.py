import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.application.use_cases.cart.add_to_cart import AddToCartUseCase
from app.domain.entities.cart import Cart


@pytest.mark.asyncio
async def test_add_to_cart_existing_cart():
    user_id = uuid4()
    product_id = uuid4()
    cart = Cart.create(user_id=user_id)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = cart

    uc = AddToCartUseCase(mock_uow, mock_repo)

    await uc.execute(user_id=user_id, product_id=product_id, quantity=2)

    assert cart.items[0].product_id == product_id
    assert cart.items[0].quantity == 2
    mock_repo.create.assert_not_awaited()
    mock_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_add_to_cart_creates_cart_if_not_exists():
    user_id = uuid4()
    product_id = uuid4()

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = None

    uc = AddToCartUseCase(mock_uow, mock_repo)

    await uc.execute(user_id=user_id, product_id=product_id, quantity=1)

    mock_repo.create.assert_awaited_once()
    mock_repo.update.assert_awaited_once()
