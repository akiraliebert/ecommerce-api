import pytest
from uuid import uuid4
from decimal import Decimal

from app.application.use_cases.checkout.checkout import CheckoutUseCase
from app.application.dto.checkout_dto import CheckoutDTO

from app.domain.entities.cart import Cart
from app.domain.entities.product import Product


@pytest.mark.asyncio
async def test_checkout_success(uow, db_session, products, carts, inventory):
    user_id = uuid4()

    product = Product.create(
        name="Test product",
        price=Decimal("10.00"),
        quantity=10
    )
    await products.create(product)

    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product.id, quantity=3)
    await carts.create(cart)

    uc = CheckoutUseCase(
        uow=uow,
        cart_repo=carts,
        product_repo=products,
        inventory_repo=inventory
    )

    reservations = await uc.execute(
        CheckoutDTO(user_id=user_id)
    )


    assert len(reservations) == 1
    assert reservations[0].product_id == product.id
    assert reservations[0].quantity == 3
    assert reservations[0].is_active is True

    updated_product = await products.get_by_id(product.id)
    assert updated_product.quantity == 7

    updated_cart = await carts.get_by_user_id(user_id)
    assert updated_cart.items == []
