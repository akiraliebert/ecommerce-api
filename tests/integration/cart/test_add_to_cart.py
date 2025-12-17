import pytest
from uuid import uuid4

from app.application.use_cases.cart.add_to_cart import AddToCartUseCase
from app.application.use_cases.cart.get_cart import GetCartUseCase


@pytest.mark.asyncio
async def test_add_item_to_cart(uow, carts):
    user_id = uuid4()
    product_id = uuid4()

    await AddToCartUseCase(uow, carts).execute(
        user_id=user_id,
        product_id=product_id,
        quantity=3
    )

    cart = await GetCartUseCase(uow, carts).execute(user_id)

    assert len(cart.items) == 1
    assert cart.items[0].product_id == product_id
    assert cart.items[0].quantity == 3
