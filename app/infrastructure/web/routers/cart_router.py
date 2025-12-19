from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.infrastructure.web.schemas.cart_schema import CartSchema, AddCartItemRequest, UpdateCartItemRequest
from app.infrastructure.web.dependencies.cart import (
    get_add_item_uc,
    get_update_item_uc,
    get_remove_item_uc,
    get_clear_cart_uc,
    get_get_cart_uc,
)
from app.infrastructure.web.dependencies.user import get_current_user


router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/items", status_code=status.HTTP_200_OK)
async def add_item(data: AddCartItemRequest, user=Depends(get_current_user), uc=Depends(get_add_item_uc)):
    try:
        await uc.execute(user.id, data.product_id, data.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=CartSchema)
async def get_cart(user=Depends(get_current_user), uc=Depends(get_get_cart_uc)):
    cart = await uc.execute(user.id)
    return cart


@router.put("/items/{product_id}")
async def update_item(product_id: UUID, data: UpdateCartItemRequest, user=Depends(get_current_user),
                      uc=Depends(get_update_item_uc)):
    try:
        await uc.execute(user.id, product_id, data.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/items/{product_id}", status_code=204)
async def remove_item(product_id: UUID, user=Depends(get_current_user), uc=Depends(get_remove_item_uc)):
    try:
        await uc.execute(user.id, product_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/", status_code=204)
async def clear_cart(user=Depends(get_current_user), uc=Depends(get_clear_cart_uc)):
    await uc.execute(user.id)
