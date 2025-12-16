from fastapi import Depends

from app.domain.repositories.product_repository import ProductRepository

from app.infrastructure.web.dependencies.common import get_uow
from app.infrastructure.database.db import get_db_session
from app.infrastructure.database.repositories.product_repository_impl import ProductRepositoryImpl

from app.application.use_cases.product.create_product import CreateProductUseCase
from app.application.use_cases.product.get_product import GetProductUseCase
from app.application.use_cases.product.list_product import ListProductsUseCase
from app.application.use_cases.product.update_product import UpdateProductUseCase
from app.application.use_cases.product.delete_product import DeleteProductUseCase


def get_product_repository(session=Depends(get_db_session)) -> ProductRepository:
    return ProductRepositoryImpl(session)


async def get_create_product_uc(uow=Depends(get_uow), repo=Depends(get_product_repository)):
    return CreateProductUseCase(uow, repo)


async def get_get_product_uc(uow=Depends(get_uow), repo=Depends(get_product_repository)):
    return GetProductUseCase(uow, repo)


async def get_list_products_uc(uow=Depends(get_uow), repo=Depends(get_product_repository)):
    return ListProductsUseCase(uow, repo)


async def get_update_product_uc(uow=Depends(get_uow), repo=Depends(get_product_repository)):
    return UpdateProductUseCase(uow, repo)


async def get_delete_product_uc(uow=Depends(get_uow), repo=Depends(get_product_repository)):
    return DeleteProductUseCase(uow, repo)
