from fastapi import Depends
from app.infrastructure.database.db import get_db_session
from app.infrastructure.database.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork

from app.application.use_cases.product.create_product import CreateProductUseCase
from app.application.use_cases.product.get_product import GetProductUseCase
from app.application.use_cases.product.list_product import ListProductsUseCase
from app.application.use_cases.product.update_product import UpdateProductUseCase
from app.application.use_cases.product.delete_product import DeleteProductUseCase


async def get_uow(session=Depends(get_db_session)):
    return SqlAlchemyUnitOfWork(session)


async def get_create_product_uc(uow=Depends(get_uow)):
    return CreateProductUseCase(uow)


async def get_get_product_uc(uow=Depends(get_uow)):
    return GetProductUseCase(uow)


async def get_list_products_uc(uow=Depends(get_uow)):
    return ListProductsUseCase(uow)


async def get_update_product_uc(uow=Depends(get_uow)):
    return UpdateProductUseCase(uow)


async def get_delete_product_uc(uow=Depends(get_uow)):
    return DeleteProductUseCase(uow)
