from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID

from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User

from app.infrastructure.web.dependencies.common import get_uow
from app.infrastructure.database.db import get_db_session
from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from app.domain.uow.unit_of_work import UnitOfWork
from app.infrastructure.security.password_hasher import PasswordHasher
from app.infrastructure.security.jwt_service import JWTService
from app.config.settings import settings

from app.application.use_cases.user.register_user import RegisterUserUseCase
from app.application.use_cases.user.authenticate_user import AuthenticateUserUseCase


security = HTTPBearer(auto_error=False)


def get_user_repository(session=Depends(get_db_session)) -> UserRepository:
    return UserRepositoryImpl(session)


def get_password_hasher():
    return PasswordHasher()


def get_jwt_service():
    return JWTService(settings.jwt_secret_access, settings.jwt_secret_refresh)


def get_register_user_uc(uow=Depends(get_uow), repo=Depends(get_user_repository),
                         password_hasher=Depends(get_password_hasher)):
    return RegisterUserUseCase(uow, repo, password_hasher)


def get_authenticate_user_uc(uow=Depends(get_uow), repo=Depends(get_user_repository),
                         password_hasher=Depends(get_password_hasher)):
    return AuthenticateUserUseCase(uow, repo, password_hasher)



async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service),
    uow: UnitOfWork = Depends(get_uow),
    user_repo=Depends(get_user_repository),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = credentials.credentials

    try:
        payload = jwt_service.decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    try:
        user_id = UUID(payload.get("sub"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
        )

    async with uow:
        user = await user_repo.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )

        return user
