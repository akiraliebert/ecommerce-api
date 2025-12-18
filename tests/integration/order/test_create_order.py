import pytest
from uuid import uuid4
from decimal import Decimal

from app.application.use_cases.order.create_order import CreateOrderUseCase
from app.application.dto.order_dto import CreateOrderDTO
from app.domain.entities.product import Product
from app.domain.entities.cart import Cart
from app.domain.entities.order import OrderStatus


@pytest.mark.asyncio
async def test_create_order_success(uow, db_session, products, carts, inventory, orders):
    user_id = uuid4()

    # --- подготовка данных как на проде ---
    async with db_session.begin():
        product = Product.create(
            name="Book",
            price=Decimal("10.00"),
            quantity=5,
        )
        await products.create(product)

        cart = Cart.create(user_id=user_id)
        cart.add_item(product_id=product.id, quantity=2)
        await carts.create(cart)

    uc = CreateOrderUseCase(
        uow=uow,
        cart_repo=carts,
        product_repo=products,
        order_repo=orders,
    )

    # --- Act ---
    result = await uc.execute(
        CreateOrderDTO(user_id=user_id)
    )

    # --- Assert ---
    assert result.user_id == user_id
    assert len(result.items) == 1
    assert result.items[0].product_id == product.id
    assert result.items[0].quantity == 2
    assert result.total == Decimal("20.00")

    # order сохранён в БД
    order_in_db = await orders.get_by_id(result.id)
    assert order_in_db is not None
    assert order_in_db.status == OrderStatus.CREATED

    # cart очищен
    cart_after = await carts.get_by_user_id(user_id)
    assert cart_after.items == []


@pytest.mark.asyncio
async def test_create_order_empty_cart(uow, products, carts, orders):
    user_id = uuid4()

    uc = CreateOrderUseCase(
        uow=uow,
        cart_repo=carts,
        product_repo=products,
        order_repo=orders,
    )

    with pytest.raises(ValueError, match="Cart is empty"):
        await uc.execute(CreateOrderDTO(user_id=user_id))

    # order не создан
    orders = await orders.get_by_user_id(user_id)
    assert orders == []


@pytest.mark.asyncio
async def test_create_order_product_not_found(uow, db_session, carts, products, orders):
    user_id = uuid4()

    async with db_session.begin():
        cart = Cart.create(user_id=user_id)
        cart.add_item(product_id=uuid4(), quantity=1)
        await carts.create(cart)

    uc = CreateOrderUseCase(
        uow=uow,
        cart_repo=carts,
        product_repo=products,
        order_repo=orders,
    )

    with pytest.raises(ValueError, match="Product not found"):
        await uc.execute(CreateOrderDTO(user_id=user_id))

    # cart не очищен (rollback)
    cart_after = await carts.get_by_user_id(user_id)
    assert len(cart_after.items) == 1
