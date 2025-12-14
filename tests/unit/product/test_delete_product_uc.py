import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from decimal import Decimal

from app.application.use_cases.product.delete_product import DeleteProductUseCase
from app.domain.entities.product import Product


@pytest.mark.asyncio
async def test_delete_product_success():
    product_id = uuid4()

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.products.get_by_id.return_value = Product(
        id=product_id,
        name="Test",
        description=None,
        price=Decimal("10.00"),
        quantity=1,
    )

    uc = DeleteProductUseCase(mock_uow)

    await uc.execute(product_id)

    mock_uow.products.delete.assert_called_once_with(product_id)

@pytest.mark.asyncio
async def test_delete_product_not_found():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.products.get_by_id.return_value = None

    uc = DeleteProductUseCase(mock_uow)

    with pytest.raises(ValueError, match="Product not found"):
        await uc.execute(uuid4())

    mock_uow.products.delete.assert_not_called()
