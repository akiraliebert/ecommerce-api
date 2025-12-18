from app.domain.entities.order import Order, OrderItem
from app.domain.uow.unit_of_work import UnitOfWork
from app.domain.repositories.cart_repository import CartRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.order_repository import OrderRepository
from app.application.dto.order_dto import (
    CreateOrderDTO,
    OrderDTO,
    OrderItemDTO,
)


class CreateOrderUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        cart_repo: CartRepository,
        product_repo: ProductRepository,
        order_repo: OrderRepository,
    ):
        self.uow = uow
        self.carts = cart_repo
        self.products = product_repo
        self.orders = order_repo


    async def execute(self, data: CreateOrderDTO) -> OrderDTO:
        async with self.uow:
            cart = await self.carts.get_by_user_id(data.user_id)

            if not cart or not cart.items:
                raise ValueError("Cart is empty")

            order_items: list[OrderItem] = []

            for item in cart.items:
                product = await self.products.get_by_id(item.product_id)

                if not product:
                    raise ValueError("Product not found")

                order_items.append(
                    OrderItem(
                        product_id=product.id,
                        quantity=item.quantity,
                        price=product.price,
                    )
                )

            order = Order.create(
                user_id=data.user_id,
                items=order_items
            )

            await self.orders.create(order)

            cart.clear()
            await self.carts.update(cart)

            return OrderDTO(
                id=order.id,
                user_id=order.user_id,
                status=order.status,
                created_at=order.created_at,
                items=[
                    OrderItemDTO(
                        product_id=i.product_id,
                        quantity=i.quantity,
                        price=i.price
                    )
                    for i in order.items
                ],
                total=order.total_amount()

            )