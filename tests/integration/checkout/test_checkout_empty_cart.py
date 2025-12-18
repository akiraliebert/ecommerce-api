import pytest
from uuid import uuid4

from app.application.use_cases.checkout.checkout import CheckoutUseCase
from app.application.dto.checkout_dto import CheckoutDTO

from app.domain.entities.cart import Cart


@pytest.mark.asyncio
async def test_checkout_empty_cart(uow, db_session, products, carts, inventory):
    user_id = uuid4()

    cart = Cart.create(user_id=user_id)
    await carts.create(cart)

    uc = CheckoutUseCase(
        uow=uow,
        cart_repo=carts,
        product_repo=products,
        inventory_repo=inventory
    )

    with pytest.raises(ValueError, match="Cart is empty"):
        await uc.execute(CheckoutDTO(user_id=user_id))
