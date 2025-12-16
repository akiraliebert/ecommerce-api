import pytest
from unittest.mock import AsyncMock
from decimal import Decimal

from app.application.use_cases.product.create_product import CreateProductUseCase
from app.application.dto.product_dto import CreateProductDTO
from app.domain.entities.product import Product


@pytest.mark.asyncio
async def test_create_product_use_case_success():
    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_repo = AsyncMock()
    mock_repo.create.return_value = Product.create(
        name="Test",
        description="Test",
        price=Decimal("10"),
        quantity=5,
    )

    uc = CreateProductUseCase(mock_uow, mock_repo)

    result = await uc.execute(
        CreateProductDTO(
            name="Test",
            description="Test",
            price=Decimal("10"),
            quantity=5,
        )
    )

    assert result.name == "Test"
    mock_repo.create.assert_called_once()