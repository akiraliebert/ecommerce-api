from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.uow.unit_of_work import UnitOfWork
from app.infrastructure.database.repositories.product_repository_impl import ProductRepositoryImpl


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.products = ProductRepositoryImpl(session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()