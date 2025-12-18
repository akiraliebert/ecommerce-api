from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.entities.order import Order, OrderItem, OrderStatus
from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.database.models.order_model import OrderModel
from app.infrastructure.database.models.order_item_model import OrderItemModel


class OrderRepositoryImpl(OrderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    # -------------------------
    # MAPPERS
    # -------------------------

    def _to_domain(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            user_id=model.user_id,
            status=OrderStatus(model.status),
            created_at=model.created_at,
            items=[
                OrderItem(
                    product_id=i.product_id,
                    quantity=i.quantity,
                    price=i.price,
                )
                for i in model.items
            ])

    def _to_model(self, order: Order) -> OrderModel:
        order_model = OrderModel(
            id=order.id,
            user_id=order.user_id,
            status=order.status.value,
            created_at=order.created_at,
        )

        order_model.items = [
            OrderItemModel(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in order.items
        ]

        return order_model


    async def create(self, order: Order) -> None:
        self.session.add(self._to_model(order))

    async def get_by_id(self, order_id):
        stmt = (
            select(OrderModel)
            .where(OrderModel.id == order_id)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._to_domain(model)
