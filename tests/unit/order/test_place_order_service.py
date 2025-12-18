import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from decimal import Decimal
from datetime import datetime, timezone

from app.application.services.order.place_order import PlaceOrderService
from app.application.dto.order_dto import PlaceOrderDTO
from app.domain.entities.cart import Cart
from app.domain.entities.product import Product
from app.domain.entities.order import OrderStatus
from app.domain.entities.inventory import InventoryReservation


@pytest.mark.asyncio
async def test_place_order_success():
    user_id = uuid4()

    product = Product.create(
        name="Test",
        price=Decimal("10.00"),
        quantity=5,
    )

    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product.id, quantity=2)


    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    carts = AsyncMock()
    carts.get_by_user_id.return_value = cart

    products = AsyncMock()
    products.get_by_id.return_value = product

    inventory = AsyncMock()
    inventory.create.return_value = InventoryReservation.create(
        product_id=product.id,
        quantity=2,
    )

    orders = AsyncMock()

    service = PlaceOrderService(
        uow=mock_uow,
        cart_repo=carts,
        product_repo=products,
        inventory_repo=inventory,
        order_repo=orders,
    )

    result = await service.execute(
        PlaceOrderDTO(user_id=user_id)
    )

    # --------- assertions ---------
    assert result.user_id == user_id
    assert result.total == Decimal("20.00")
    assert result.status == OrderStatus.CREATED
    assert len(result.items) == 1

    carts.get_by_user_id.assert_awaited_once_with(user_id)
    products.get_by_id.assert_awaited_once_with(product.id)
    inventory.create.assert_awaited_once()
    orders.create.assert_awaited_once()
    carts.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_place_order_empty_cart():
    user_id = uuid4()

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    carts = AsyncMock()
    carts.get_by_user_id.return_value = None

    service = PlaceOrderService(
        uow=mock_uow,
        cart_repo=carts,
        product_repo=AsyncMock(),
        inventory_repo=AsyncMock(),
        order_repo=AsyncMock(),
    )

    with pytest.raises(ValueError, match="Cart is empty"):
        await service.execute(PlaceOrderDTO(user_id=user_id))


@pytest.mark.asyncio
async def test_place_order_insufficient_stock():
    user_id = uuid4()
    product_id = uuid4()

    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product_id, quantity=10)

    product = Product.create(
        name="Test",
        price=Decimal("10.00"),
        quantity=2,
    )

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    carts = AsyncMock()
    carts.get_by_user_id.return_value = cart

    products = AsyncMock()
    products.get_by_id.return_value = product

    service = PlaceOrderService(
        uow=mock_uow,
        cart_repo=carts,
        product_repo=products,
        inventory_repo=AsyncMock(),
        order_repo=AsyncMock(),
    )

    with pytest.raises(ValueError, match="Not enough product in stock"):
        await service.execute(PlaceOrderDTO(user_id=user_id))


@pytest.mark.asyncio
async def test_place_order_product_not_found():
    user_id = uuid4()
    product_id = uuid4()

    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product_id, quantity=1)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    carts = AsyncMock()
    carts.get_by_user_id.return_value = cart

    products = AsyncMock()
    products.get_by_id.return_value = None

    service = PlaceOrderService(
        uow=mock_uow,
        cart_repo=carts,
        product_repo=products,
        inventory_repo=AsyncMock(),
        order_repo=AsyncMock(),
    )

    with pytest.raises(ValueError, match="Product not found"):
        await service.execute(PlaceOrderDTO(user_id=user_id))


