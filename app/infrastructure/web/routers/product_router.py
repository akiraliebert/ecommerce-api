from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.infrastructure.web.schemas.product_schema import (
    ProductCreateSchema,
    ProductResponseSchema,
    ProductUpdateSchema
)

from app.infrastructure.web.dependencies.product import (
    get_create_product_uc,
    get_get_product_uc,
    get_list_products_uc,
    get_update_product_uc,
    get_delete_product_uc
)
from app.domain.entities.user import User
from app.infrastructure.web.dependencies.user import get_current_user


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponseSchema)
async def create_product(data: ProductCreateSchema, use_case=Depends(get_create_product_uc),
                         current_user: User = Depends(get_current_user)):
    return await use_case.execute(data)


@router.get("/", response_model=list[ProductResponseSchema])
async def list_products(
    use_case = Depends(get_list_products_uc)
):
    return await use_case.execute()


@router.get("/{product_id}", response_model=ProductResponseSchema)
async def get_product(
    product_id: UUID,
    use_case = Depends(get_get_product_uc)
):
    try:
        return await use_case.execute(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@router.put("/{product_id}", response_model=ProductResponseSchema)
async def update_product(
    product_id: UUID,
    data: ProductUpdateSchema,
    use_case=Depends(get_update_product_uc),
    current_user: User = Depends(get_current_user)
):
    try:
        return await use_case.execute(product_id, data)
    except ValueError as e:
        if str(e) == "No fields provided for update":
            raise HTTPException(status_code=400, detail=str(e))
        if str(e) == "Product not found":
            raise HTTPException(status_code=404, detail=str(e))
        raise


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID,
    use_case=Depends(get_delete_product_uc),
    current_user: User = Depends(get_current_user)
):
    try:
        await use_case.execute(product_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
