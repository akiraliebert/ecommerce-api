from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.models.base import Base


class CartModel(Base):
    __tablename__ = "carts"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(unique=True, index=True)

    items: Mapped[list["CartItemModel"]] = relationship(
        back_populates="cart",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
