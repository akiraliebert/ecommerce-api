from uuid import UUID

from app.domain.uow.unit_of_work import UnitOfWork
from app.domain.repositories.order_repository import OrderRepository
from app.application.dto.order_dto import OrderDTO


class GetOrderByIdUseCase:
    def __init__(self, uow: UnitOfWork, order_repo: OrderRepository):
        self.uow = uow
        self.orders = order_repo

    async def execute(self, order_id: UUID, user_id: UUID) -> OrderDTO:
        async with self.uow:
            order = await self.orders.get_by_id(order_id)

            if not order or order.user_id != user_id:
                raise ValueError("Order not found")

            return OrderDTO.from_domain(order)