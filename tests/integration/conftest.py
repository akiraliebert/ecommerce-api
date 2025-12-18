import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.infrastructure.database.repositories.product_repository_impl import ProductRepositoryImpl
from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.database.repositories.cart_repository_impl import CartRepositoryImpl
from app.infrastructure.database.repositories.inventory_repository_impl import InventoryRepositoryImpl
from app.config.settings import settings


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(settings.database_url, echo=True)
    async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture
async def uow(db_session):
    return SqlAlchemyUnitOfWork(db_session)


@pytest_asyncio.fixture
async def products(db_session):
    return ProductRepositoryImpl(db_session)


@pytest_asyncio.fixture
async def users(db_session):
    return UserRepositoryImpl(db_session)


@pytest_asyncio.fixture
async def carts(db_session):
    return CartRepositoryImpl(db_session)


@pytest_asyncio.fixture
async def inventory(db_session):
    return InventoryRepositoryImpl(db_session)
