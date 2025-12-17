from fastapi import APIRouter, Depends

from app.domain.entities.user import User
from app.infrastructure.web.dependencies.user import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
