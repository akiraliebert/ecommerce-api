from uuid import UUID
from typing import Optional

from sqlalchemy import select

from app.domain.entities.inventory import InventoryReservation
from app.domain.repositories.inventory_repository import InventoryRepository
from app.infrastructure.database.models.inventory_model import InventoryReservationModel


class InventoryRepositoryImpl(InventoryRepository):
    def __init__(self, session):
        self.session = session

    # -------------------------
    # MAPPERS
    # -------------------------

    def _to_domain(self, model: InventoryReservationModel) -> InventoryReservation:
        return InventoryReservation(
            id=model.id,
            product_id=model.product_id,
            quantity=model.quantity,
            is_active=model.is_active,
        )

    def _to_model(self, reservation: InventoryReservation) -> InventoryReservationModel:
        return InventoryReservationModel(
            id=reservation.id,
            product_id=reservation.product_id,
            quantity=reservation.quantity,
            is_active=reservation.is_active,
        )

    async def get_by_id(self, reservation_id: UUID) -> Optional[InventoryReservation]:
        result = await self.session.execute(
            select(InventoryReservationModel)
            .where(InventoryReservationModel.id == reservation_id)
        )
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self._to_domain(model)

    async def get_active_by_product_id(
        self,
        product_id: UUID
    ) -> list[InventoryReservation]:
        result = await self.session.execute(
            select(InventoryReservationModel)
            .where(
                InventoryReservationModel.product_id == product_id,
                InventoryReservationModel.is_active.is_(True)
            )
        )

        return [self._to_domain(m) for m in result.scalars().all()]

    async def create(self, reservation: InventoryReservation) -> None:
        model = self._to_model(reservation)
        self.session.add(model)

    async def update(self, reservation: InventoryReservation) -> None:
        result = await self.session.execute(
            select(InventoryReservationModel)
            .where(InventoryReservationModel.id == reservation.id)
        )
        model = result.scalar_one()

        model.quantity = reservation.quantity
        model.is_active = reservation.is_active
