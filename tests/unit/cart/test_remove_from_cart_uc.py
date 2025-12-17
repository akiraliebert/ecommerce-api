import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.application.use_cases.cart.remove_from_cart import RemoveFromCartUseCase
from app.domain.entities.cart import Cart


@pytest.mark.asyncio
async def test_remove_from_cart_success():
    user_id = uuid4()
    product_id = uuid4()
    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product_id, quantity=3)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = cart

    uc = RemoveFromCartUseCase(mock_uow, mock_repo)

    await uc.execute(user_id=user_id, product_id=product_id)

    assert cart.items == []
    mock_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_remove_from_cart_not_found():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_repo = AsyncMock()
    mock_repo.get_by_user_id.return_value = None

    uc = RemoveFromCartUseCase(mock_uow, mock_repo)
    with pytest.raises(ValueError, match="Cart not found"):
        await uc.execute(user_id=uuid4(), product_id=uuid4())
