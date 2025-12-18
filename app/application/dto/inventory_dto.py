from dataclasses import dataclass
from uuid import UUID

@dataclass
class ReleaseInventoryDTO:
    reservation_id: UUID