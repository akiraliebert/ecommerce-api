import pytest
from uuid import uuid4
from decimal import Decimal

from app.application.services.order.place_order import PlaceOrderService
from app.application.dto.order_dto import PlaceOrderDTO
from app.domain.entities.product import Product
from app.domain.entities.cart import Cart
from app.domain.entities.order import OrderStatus


@pytest.mark.asyncio
async def test_place_order_success(
    uow,
    db_session,
    products,
    carts,
    inventory,
    orders,
):
    user_id = uuid4()


    async with db_session.begin():
        product = Product.create(
            name="Book",
            price=Decimal("15.00"),
            quantity=10,
        )
        await products.create(product)

        cart = Cart.create(user_id=user_id)
        cart.add_item(product_id=product.id, quantity=2)
        await carts.create(cart)

    service = PlaceOrderService(
        uow=uow,
        cart_repo=carts,
        product_repo=products,
        inventory_repo=inventory,
        order_repo=orders,
    )


    result = await service.execute(
        PlaceOrderDTO(user_id=user_id)
    )


    assert result.user_id == user_id
    assert result.total == Decimal("30.00")
    assert result.status == OrderStatus.CREATED
    assert len(result.items) == 1


    product_after = await products.get_by_id(product.id)
    assert product_after.quantity == 8  # reserve worked

    cart_after = await carts.get_by_user_id(user_id)
    assert cart_after.items == []

    user_orders = await orders.get_by_user_id(user_id)
    assert len(user_orders) == 1


@pytest.mark.asyncio
async def test_place_order_insufficient_stock_rollback(
    uow,
    db_session,
    products,
    carts,
    inventory,
    orders
):
    user_id = uuid4()

    async with db_session.begin():
        product = Product.create(
            name="Limited",
            price=Decimal("10.00"),
            quantity=2,
        )
        await products.create(product)

        cart = Cart.create(user_id=user_id)
        cart.add_item(product_id=product.id, quantity=5)
        await carts.create(cart)

    service = PlaceOrderService(
        uow=uow,
        cart_repo=carts,
        product_repo=products,
        inventory_repo=inventory,
        order_repo=orders
    )

    with pytest.raises(ValueError, match="Not enough product in stock"):
        await service.execute(
            PlaceOrderDTO(user_id=user_id)
        )


    product_after = await products.get_by_id(product.id)
    assert product_after.quantity == 2

    cart_after = await carts.get_by_user_id(user_id)
    assert len(cart_after.items) == 1
