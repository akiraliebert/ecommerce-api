import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.config.settings import settings


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(settings.database_url, echo=True)
    async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
        await session.rollback()
    await engine.dispose()


@pytest_asyncio.fixture
async def uow(db_session):
    return SqlAlchemyUnitOfWork(db_session)



