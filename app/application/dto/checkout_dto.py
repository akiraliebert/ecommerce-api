from dataclasses import dataclass
from uuid import UUID


@dataclass
class CheckoutDTO:
    user_id: UUID
