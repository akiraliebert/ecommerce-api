import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from decimal import Decimal

from app.application.use_cases.inventory.reserve_inventory import ReserveInventoryUseCase
from app.domain.entities.product import Product


@pytest.mark.asyncio
async def test_reserve_inventory_success():
    product_id = uuid4()

    product = Product.create(
        name="Test product",
        price=Decimal("10.00"),
        quantity=20
    )

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_product_repo = AsyncMock()
    mock_product_repo.get_by_id.return_value = product

    mock_inventory_repo = AsyncMock()

    uc = ReserveInventoryUseCase(
        uow=mock_uow,
        product_repo=mock_product_repo,
        inventory_repo=mock_inventory_repo
    )

    reservation = await uc.execute(product_id=product_id, quantity=5)

    assert reservation.product_id == product_id
    assert reservation.quantity == 5
    assert reservation.is_active is True

    # доменная логика сработала
    assert product.quantity == 15

    mock_product_repo.get_by_id.assert_awaited_once_with(product_id)
    mock_inventory_repo.create.assert_awaited_once()
    mock_product_repo.update.assert_awaited_once_with(product)


@pytest.mark.asyncio
async def test_reserve_inventory_product_not_found():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_product_repo = AsyncMock()
    mock_product_repo.get_by_id.return_value = None

    mock_inventory_repo = AsyncMock()

    uc = ReserveInventoryUseCase(
        uow=mock_uow,
        product_repo=mock_product_repo,
        inventory_repo=mock_inventory_repo
    )

    with pytest.raises(ValueError, match="Product not found"):
        await uc.execute(product_id=uuid4(), quantity=5)

    mock_inventory_repo.create.assert_not_called()


@pytest.mark.asyncio
async def test_reserve_inventory_not_enough_stock():
    product = Product.create(
        name="Test product",
        price=Decimal("10.00"),
        quantity=3
    )

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    mock_product_repo = AsyncMock()
    mock_product_repo.get_by_id.return_value = product

    mock_inventory_repo = AsyncMock()

    uc = ReserveInventoryUseCase(
        uow=mock_uow,
        product_repo=mock_product_repo,
        inventory_repo=mock_inventory_repo
    )

    with pytest.raises(ValueError, match="Not enough product in stock"):
        await uc.execute(product_id=uuid4(), quantity=10)

    # ничего не сохраняем
    mock_inventory_repo.create.assert_not_called()
    mock_product_repo.update.assert_not_called()
