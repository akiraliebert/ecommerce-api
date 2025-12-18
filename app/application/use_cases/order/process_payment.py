from app.domain.uow.unit_of_work import UnitOfWork
from app.domain.repositories.order_repository import OrderRepository
from app.domain.services.payment_service import PaymentService, PaymentResult


class ProcessPaymentUseCase:
    def __init__(
        self,
        uow: UnitOfWork,
        order_repo: OrderRepository,
        payment_service: PaymentService,
    ):
        self.uow = uow
        self.orders = order_repo
        self.payments = payment_service


    async def execute(self, order_id):
        async with self.uow:
            order = await self.orders.get_by_id(order_id)

            if not order:
                raise ValueError("Order not found")

            result = await self.payments.pay(
                order_id=order.id,
                amount=order.total_amount(),
            )

            if result is PaymentResult.SUCCESS:
                order.mark_paid()

            await self.orders.update(order)

            return order
