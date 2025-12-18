import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from decimal import Decimal

from app.application.use_cases.inventory.release_inventory import ReleaseInventoryUseCase
from app.application.dto.inventory_dto import ReleaseInventoryDTO
from app.domain.entities.inventory import InventoryReservation
from app.domain.entities.product import Product


@pytest.mark.asyncio
async def test_release_inventory_success():
    reservation = InventoryReservation.create(
        product_id=uuid4(),
        quantity=5
    )

    product = Product.create(
        name="Test",
        price=Decimal("100"),
        quantity=10
    )

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    inventory_repo = AsyncMock()
    inventory_repo.get_by_id.return_value = reservation

    product_repo = AsyncMock()
    product_repo.get_by_id.return_value = product

    uc = ReleaseInventoryUseCase(
        mock_uow,
        inventory_repo,
        product_repo,
    )

    await uc.execute(ReleaseInventoryDTO(reservation.id))

    assert reservation.is_active is False
    assert product.quantity == 15

    inventory_repo.update.assert_awaited_once()
    product_repo.update.assert_awaited_once()


@pytest.mark.asyncio
async def test_release_inventory_not_found():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    inventory_repo = AsyncMock()
    inventory_repo.get_by_id.return_value = None

    product_repo = AsyncMock()

    uc = ReleaseInventoryUseCase(
        mock_uow,
        inventory_repo,
        product_repo,
    )

    with pytest.raises(ValueError, match="Inventory reservation not found"):
        await uc.execute(ReleaseInventoryDTO(uuid4()))


@pytest.mark.asyncio
async def test_release_inventory_already_canceled():
    reservation = InventoryReservation.create(
        product_id=uuid4(),
        quantity=5
    )
    reservation.cancel()

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow

    inventory_repo = AsyncMock()
    inventory_repo.get_by_id.return_value = reservation

    product_repo = AsyncMock()

    uc = ReleaseInventoryUseCase(
        mock_uow,
        inventory_repo,
        product_repo,
    )

    with pytest.raises(ValueError, match="Inventory reservation already canceled"):
        await uc.execute(ReleaseInventoryDTO(reservation.id))

    product_repo.get_by_id.assert_not_called()
