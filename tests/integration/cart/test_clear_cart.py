import pytest
from uuid import uuid4

from app.application.use_cases.cart.add_to_cart import AddToCartUseCase
from app.application.use_cases.cart.clear_cart import ClearCartUseCase
from app.application.use_cases.cart.get_cart import GetCartUseCase


@pytest.mark.asyncio
async def test_clear_cart(uow, carts):
    user_id = uuid4()

    await AddToCartUseCase(uow, carts).execute(user_id, uuid4(), 1)
    await AddToCartUseCase(uow, carts).execute(user_id, uuid4(), 2)

    await ClearCartUseCase(uow, carts).execute(user_id)

    cart = await GetCartUseCase(uow, carts).execute(user_id)

    assert cart.items == []
