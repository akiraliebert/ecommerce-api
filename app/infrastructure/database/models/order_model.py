from sqlalchemy import DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import UUID
from datetime import datetime

from app.infrastructure.database.models.base import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(index=True)

    items: Mapped[list["OrderItemModel"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

