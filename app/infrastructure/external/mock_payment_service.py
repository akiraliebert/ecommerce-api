from app.domain.services.payment_service import PaymentService, PaymentResult


class MockPaymentService(PaymentService):
    async def pay(self, order_id, amount):
        # имитация внешнего сервиса
        return PaymentResult.SUCCESS