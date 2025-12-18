import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from decimal import Decimal

from app.application.use_cases.checkout.checkout import CheckoutUseCase
from app.application.dto.checkout_dto import CheckoutDTO
from app.domain.entities.cart import Cart, CartItem
from app.domain.entities.product import Product
from app.domain.entities.inventory import InventoryReservation


@pytest.mark.asyncio
async def test_checkout_success():
    user_id = uuid4()
    product_id = uuid4()

    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product_id, quantity=2)

    product = Product.create(
        name="Test",
        price=Decimal("100"),
        quantity=5
    )

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    cart_repo = AsyncMock()
    cart_repo.get_by_user_id.return_value = cart

    product_repo = AsyncMock()
    product_repo.get_by_id.return_value = product

    inventory_repo = AsyncMock()
    inventory_repo.create.return_value = InventoryReservation.create(
        product_id=product_id,
        quantity=2
    )

    uc = CheckoutUseCase(
        uow=mock_uow,
        cart_repo=cart_repo,
        product_repo=product_repo,
        inventory_repo=inventory_repo,
    )

    result = await uc.execute(CheckoutDTO(user_id=user_id))

    assert len(result) == 1
    assert product.quantity == 3
    cart_repo.update.assert_awaited_once()
    product_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_checkout_empty_cart():
    user_id = uuid4()

    cart = Cart.create(user_id=user_id)

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    cart_repo = AsyncMock()
    cart_repo.get_by_user_id.return_value = cart

    uc = CheckoutUseCase(
        uow=mock_uow,
        cart_repo=cart_repo,
        product_repo=AsyncMock(),
        inventory_repo=AsyncMock(),
    )

    with pytest.raises(ValueError, match="Cart is empty"):
        await uc.execute(CheckoutDTO(user_id=user_id))


@pytest.mark.asyncio
async def test_checkout_product_not_found():
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

    uc = CheckoutUseCase(
        uow=mock_uow,
        cart_repo=cart_repo,
        product_repo=product_repo,
        inventory_repo=AsyncMock(),
    )

    with pytest.raises(ValueError, match="Product not found"):
        await uc.execute(CheckoutDTO(user_id=user_id))


@pytest.mark.asyncio
async def test_checkout_not_enough_stock():
    user_id = uuid4()
    product_id = uuid4()

    cart = Cart.create(user_id=user_id)
    cart.add_item(product_id=product_id, quantity=10)

    product = Product.create(
        name="Test",
        price=Decimal("100"),
        quantity=5
    )

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    cart_repo = AsyncMock()
    cart_repo.get_by_user_id.return_value = cart

    product_repo = AsyncMock()
    product_repo.get_by_id.return_value = product

    uc = CheckoutUseCase(
        uow=mock_uow,
        cart_repo=cart_repo,
        product_repo=product_repo,
        inventory_repo=AsyncMock(),
    )

    with pytest.raises(ValueError, match="Not enough product in stock"):
        await uc.execute(CheckoutDTO(user_id=user_id))
