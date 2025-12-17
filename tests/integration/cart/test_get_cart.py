import pytest
from uuid import uuid4

from app.application.use_cases.cart.get_cart import GetCartUseCase


@pytest.mark.asyncio
async def test_get_cart_creates_new(uow, carts):
    user_id = uuid4()

    uc = GetCartUseCase(uow, carts)

    cart = await uc.execute(user_id=user_id)

    assert cart.user_id == user_id
    assert cart.items == []


@pytest.mark.asyncio
async def test_get_cart_existing(uow, carts):
    user_id = uuid4()

    cart = await GetCartUseCase(uow, carts).execute(user_id)

    cart2 = await GetCartUseCase(uow, carts).execute(user_id)

    assert cart.id == cart2.id
