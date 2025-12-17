import pytest

from app.domain.entities.user import User


@pytest.mark.asyncio
async def test_create_and_get_user(uow, users):
    async with uow:
        product = User.create(
            email="test_repo@gmail.com",
            hashed_password='dsf3kjfwijwofjs21'
        )
        created = await users.create(product)

    async with uow:
        fetched = await users.get_by_id(created.id)

        assert fetched is not None
        assert fetched.email == "test_repo@gmail.com"
        assert fetched.hashed_password == 'dsf3kjfwijwofjs21'

    async with uow:
        fetched = await users.get_by_email(created.email)

        assert fetched is not None
        assert fetched.email == "test_repo@gmail.com"
        assert fetched.hashed_password == 'dsf3kjfwijwofjs21'
