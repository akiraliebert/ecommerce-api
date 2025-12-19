from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.application.dto.user_dto import CreateUserDTO
from app.infrastructure.web.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from app.infrastructure.web.dependencies.user import get_register_user_uc, get_authenticate_user_uc, get_jwt_service


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, use_case=Depends(get_register_user_uc)):
    try:
        user = await use_case.execute(
            CreateUserDTO(
                email=data.email,
                password=data.password,
            )
        )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def register(data: LoginRequest, use_case=Depends(get_authenticate_user_uc), jwt_service=Depends(get_jwt_service)):
    try:
        user = await use_case.execute(data.email, data.password)

        return TokenResponse(
            access_token=jwt_service.create_access_token(user.id),
            refresh_token=jwt_service.create_refresh_token(user.id),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/refresh")
async def refresh(
    data: RefreshTokenRequest,
    jwt_service=Depends(get_jwt_service),
):
    try:
        payload = jwt_service.decode_refresh_token(data.refresh_token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if payload.get("type") != "refresh":
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

    return TokenResponse(
        access_token=jwt_service.create_access_token(user_id),
        refresh_token=jwt_service.create_refresh_token(user_id),
    )
