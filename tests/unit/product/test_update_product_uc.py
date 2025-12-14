import pytest
from unittest.mock import AsyncMock
from decimal import Decimal
from uuid import uuid4

from app.application.use_cases.product.update_product import UpdateProductUseCase
from app.application.dto.product_dto import UpdateProductDTO
from app.domain.entities.product import Product


@pytest.mark.asyncio
async def test_update_product_success():
    product_id = uuid4()

    existing_product = Product(
        id=product_id,
        name="Old name",
        description="Old desc",
        price=Decimal("10"),
        quantity=5,
    )

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.products.get_by_id.return_value = existing_product
    mock_uow.products.update.return_value = existing_product

    uc = UpdateProductUseCase(mock_uow)

    result = await uc.execute(
        product_id,
        UpdateProductDTO(
            name="New name",
            price=Decimal("20"),
        ),
    )

    assert result.name == "New name"
    assert result.price == Decimal("20")

    mock_uow.products.get_by_id.assert_called_once_with(product_id)
    mock_uow.products.update.assert_called_once()

@pytest.mark.asyncio
async def test_update_product_not_found():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.products.get_by_id.return_value = None

    uc = UpdateProductUseCase(mock_uow)

    with pytest.raises(ValueError, match="Product not found"):
        await uc.execute(
            uuid4(),
            UpdateProductDTO(name="New"),
        )

    mock_uow.products.update.assert_not_called()

@pytest.mark.asyncio
async def test_update_product_no_fields_provided():
    mock_uow = AsyncMock()
    uc = UpdateProductUseCase(mock_uow)

    with pytest.raises(ValueError, match="No fields provided for update"):
        await uc.execute(
            uuid4(),
            UpdateProductDTO(),
        )
