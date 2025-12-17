import pytest
from uuid import uuid4

from app.application.use_cases.cart.add_to_cart import AddToCartUseCase
from app.application.use_cases.cart.update_cart_item import UpdateCartItemUseCase
from app.application.use_cases.cart.get_cart import GetCartUseCase


@pytest.mark.asyncio
async def test_update_cart_item(uow, carts):
    user_id = uuid4()
    product_id = uuid4()

    await AddToCartUseCase(uow, carts).execute(user_id, product_id, 2)
    await UpdateCartItemUseCase(uow, carts).execute(user_id, product_id, 10)

    cart = await GetCartUseCase(uow, carts).execute(user_id)

    assert cart.items[0].quantity == 10
