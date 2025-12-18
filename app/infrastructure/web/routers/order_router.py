from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from app.infrastructure.web.schemas.order_schema import OrderResponse
from app.application.dto.order_dto import PlaceOrderDTO
from app.infrastructure.web.dependencies.order import (
    get_place_order_service,
    get_my_orders_uc,
    get_order_by_id_uc,
    get_process_payment_uc,
    get_cancel_order_uc
)
from app.infrastructure.web.dependencies.user import get_current_user
from app.application.dto.order_dto import OrderDTO


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
async def place_order(user=Depends(get_current_user), service=Depends(get_place_order_service)):
    try:
        return await service.execute(
            PlaceOrderDTO(user_id=user.id)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=list[OrderDTO])
async def get_my_orders(
    user=Depends(get_current_user),
    uc=Depends(get_my_orders_uc),
):
    return await uc.execute(user.id)


@router.get("/{order_id}", response_model=OrderDTO)
async def get_order(
    order_id: UUID,
    user=Depends(get_current_user),
    uc=Depends(get_order_by_id_uc),
):
    try:
        return await uc.execute(order_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{order_id}/pay", response_model=OrderResponse)
async def pay_order(order_id: UUID, uc=Depends(get_process_payment_uc)):
    try:
        return await uc.execute(order_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{order_id}/cancel", status_code=204)
async def cancel_order(order_id: UUID, user=Depends(get_current_user), uc=Depends(get_cancel_order_uc)):
    try:
        await uc.execute(order_id, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

