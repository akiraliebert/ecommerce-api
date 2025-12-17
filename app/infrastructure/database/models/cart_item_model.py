from uuid import UUID

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base


class CartItemModel(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    cart_id: Mapped[UUID] = mapped_column(
        ForeignKey("carts.id", ondelete="CASCADE"),
        index=True
    )

    product_id: Mapped[UUID] = mapped_column(index=True)
    quantity: Mapped[int] = mapped_column(Integer)

    cart: Mapped["CartModel"] = relationship(back_populates="items")
