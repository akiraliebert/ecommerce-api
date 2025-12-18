from uuid import UUID

from sqlalchemy import Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.models.base import Base


class InventoryReservationModel(Base):
    __tablename__ = "inventory_reservations"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),  # Предотвращаем удаление товара админом ЕСЛИ есть активные резеры
        index=True,
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
