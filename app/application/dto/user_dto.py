from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class CreateUserDTO:
    email: str
    password: str


@dataclass
class UserDTO:
    id: UUID
    email: str
    is_active: bool
    created_at: datetime
