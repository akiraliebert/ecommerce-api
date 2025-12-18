import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from decimal import Decimal

from app.application.use_cases.order.create_order import CreateOrderUseCase
from app.application.dto.order_dto import CreateOrderDTO
from app.domain.entities.cart import Cart
from app.domain.entities.product import Product


@pytest.mark.asyncio
async def test_create_order_success():
    user_id = uuid4()

    product = Product.create(
        name="Test",
        price=Decimal("10.00"),
        quantity=100
    )

    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product.id, quantity=2)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    cart_repo = AsyncMock()
    cart_repo.get_by_user_id.return_value = cart

    product_repo = AsyncMock()
    product_repo.get_by_id.return_value = product

    order_repo = AsyncMock()

    uc = CreateOrderUseCase(
        uow=mock_uow,
        cart_repo=cart_repo,
        product_repo=product_repo,
        order_repo=order_repo
    )

    result = await uc.execute(CreateOrderDTO(user_id=user_id))

    assert result.user_id == user_id
    assert len(result.items) == 1
    assert result.total == Decimal("20.00")

    order_repo.create.assert_awaited_once()
    cart_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_order_cart_empty():
    user_id = uuid4()

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    cart_repo = AsyncMock()
    cart_repo.get_by_user_id.return_value = None

    product_repo = AsyncMock()
    order_repo = AsyncMock()

    uc = CreateOrderUseCase(
        uow=mock_uow,
        cart_repo=cart_repo,
        product_repo=product_repo,
        order_repo=order_repo
    )

    with pytest.raises(ValueError, match="Cart is empty"):
        await uc.execute(CreateOrderDTO(user_id=user_id))

    order_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_create_order_product_not_found():
    user_id = uuid4()
    product_id = uuid4()

    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product_id, quantity=1)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    cart_repo = AsyncMock()
    cart_repo.get_by_user_id.return_value = cart

    product_repo = AsyncMock()
    product_repo.get_by_id.return_value = None

    order_repo = AsyncMock()

    uc = CreateOrderUseCase(
        uow=mock_uow,
        cart_repo=cart_repo,
        product_repo=product_repo,
        order_repo=order_repo
    )

    with pytest.raises(ValueError, match="Product not found"):
        await uc.execute(CreateOrderDTO(user_id=user_id))

    order_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_cart_is_cleared_after_order():
    user_id = uuid4()

    product = Product.create(
        name="Test",
        price=Decimal("5.00"),
        quantity=10
    )

    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product.id, quantity=1)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    cart_repo = AsyncMock()
    cart_repo.get_by_user_id.return_value = cart

    product_repo = AsyncMock()
    product_repo.get_by_id.return_value = product

    order_repo = AsyncMock()

    uc = CreateOrderUseCase(
        uow=mock_uow,
        cart_repo=cart_repo,
        product_repo=product_repo,
        order_repo=order_repo
    )

    await uc.execute(CreateOrderDTO(user_id=user_id))

    assert cart.items == []


