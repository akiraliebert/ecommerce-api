from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID
from decimal import Decimal


class PaymentResult(Enum):
    SUCCESS = "success"
    FAILED = "failed"


class PaymentService(ABC):
    @abstractmethod
    async def pay(
        self,
        order_id: UUID,
        amount: Decimal,
    ) -> PaymentResult:
        pass
