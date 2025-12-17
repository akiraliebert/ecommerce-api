import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.application.use_cases.cart.update_cart_item import UpdateCartItemUseCase
from app.domain.entities.cart import Cart


@pytest.mark.asyncio
async def test_update_cart_item_success():
    user_id = uuid4()
    product_id = uuid4()
    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product_id, quantity=2)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = cart

    uc = UpdateCartItemUseCase(mock_uow, mock_repo)

    await uc.execute(user_id=user_id, product_id=product_id, quantity=5)

    assert cart.items[0].quantity == 5
    mock_repo.create.assert_not_awaited()
    mock_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_cart_item_cart_not_found():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = None

    uc = UpdateCartItemUseCase(mock_uow, mock_repo)

    with pytest.raises(ValueError, match="Cart not found"):
        await uc.execute(user_id=uuid4(), product_id=uuid4(), quantity=1)
