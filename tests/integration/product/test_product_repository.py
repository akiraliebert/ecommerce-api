import pytest
from decimal import Decimal

from app.domain.entities.product import Product


@pytest.mark.asyncio
async def test_create_and_get_product(uow, products):
    async with uow:
        product = Product.create(
            name="Integration test",
            price=Decimal("15.50"),
            quantity=3,
            description="Test",
        )
        created = await products.create(product)

    async with uow:
        fetched = await products.get_by_id(created.id)

        assert fetched is not None
        assert fetched.name == "Integration test"
        assert fetched.price == Decimal("15.50")


@pytest.mark.asyncio
async def test_list_products(uow, products):
    async with uow:
        await products.create(
            Product.create(name="P1", price=Decimal("10"), quantity=1)
        )
        await products.create(
            Product.create(name="P2", price=Decimal("20"), quantity=2)
        )

    async with uow:
        products = await products.list()
        names = [p.name for p in products]

        assert "P1" in names
        assert "P2" in names


@pytest.mark.asyncio
async def test_update_product(uow, products):
    async with uow:
        product = await products.create(
            Product.create(name="Old", price=Decimal("10"), quantity=1)
        )

    async with uow:
        product.price = Decimal("99")
        await products.update(product)

    async with uow:
        updated = await products.get_by_id(product.id)
        assert updated.price == Decimal("99")


@pytest.mark.asyncio
async def test_delete_product(uow, products):
    async with uow:
        product = await products.create(
            Product.create(name="To delete", price=Decimal("5"), quantity=1)
        )

    async with uow:
        await products.delete(product.id)

    async with uow:
        result = await products.get_by_id(product.id)
        assert result is None

@pytest.mark.asyncio
async def test_transaction_rollback(uow, products):
    try:
        async with uow:
            await products.create(
                Product.create(name="Rollback", price=Decimal("10"), quantity=1)
            )
            raise RuntimeError("Boom")
    except RuntimeError:
        pass

    async with uow:
        products = await products.list()
        names = [p.name for p in products]

        assert "Rollback" not in names
