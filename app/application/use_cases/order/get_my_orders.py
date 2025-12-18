from uuid import UUID

from app.domain.uow.unit_of_work import UnitOfWork
from app.domain.repositories.order_repository import OrderRepository

from app.application.dto.order_dto import (
    OrderDTO,
)


class GetMyOrdersUseCase:
    def __init__(self, uow: UnitOfWork, order_repo: OrderRepository):
        self.uow = uow
        self.orders = order_repo

    async def execute(self, user_id: UUID) -> list[OrderDTO]:
        async with self.uow:
            orders = await self.orders.get_by_user_id(user_id)

            return [
                OrderDTO.from_domain(order)
                for order in orders
            ]
