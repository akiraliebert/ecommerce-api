import pytest
from uuid import uuid4
from decimal import Decimal

from app.application.use_cases.checkout.checkout import CheckoutUseCase
from app.application.dto.checkout_dto import CheckoutDTO

from app.domain.entities.cart import Cart
from app.domain.entities.product import Product


@pytest.mark.asyncio
async def test_checkout_insufficient_stock(uow, db_session, products, carts, inventory):
    user_id = uuid4()

    # имитируем реальную ситуацию на проде, иначе в тестах весь setup идет в рамках одного db_session
    # что означает ValueError == rollback и созданный продукт откатывается. Поэтому делаем async with db_session.begin()
    async with db_session.begin():
        product = Product.create(
            name="Limited",
            price=Decimal("10.00"),
            quantity=2
        )
        await products.create(product)

        cart = Cart.create(user_id=user_id)
        cart.add_item(product_id=product.id, quantity=5)
        await carts.create(cart)

    uc = CheckoutUseCase(
        uow=uow,
        cart_repo=carts,
        product_repo=products,
        inventory_repo=inventory
    )

    with pytest.raises(ValueError, match="Not enough product in stock"):
        await uc.execute(CheckoutDTO(user_id=user_id))


    # ❗ проверяем rollback
    product_after = await products.get_by_id(product.id)
    assert product_after.quantity == 2

    cart_after = await carts.get_by_user_id(user_id)
    assert len(cart_after.items) == 1
