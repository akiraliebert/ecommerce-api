from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    # ---------------------------
    #   Helpers (private)
    # ---------------------------

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        """Преобразование SQLAlchemy модели в доменную сущность."""
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at
        )

    @staticmethod
    def _to_model(entity: User) -> UserModel:
        """Преобразование domain сущности в SQLAlchemy модель."""
        return UserModel(
            id=entity.id,
            email=entity.email,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
            created_at=entity.created_at
        )


    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            return self._to_entity(model)
        return None


    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            return self._to_entity(model)
        return None

    async def create(self, user: User) -> None:
        model = self._to_model(user)
        self.session.add(model)
