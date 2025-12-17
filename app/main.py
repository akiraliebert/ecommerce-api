from fastapi import FastAPI


from app.infrastructure.web.routers.product_router import router as product_router
from app.infrastructure.web.routers.auth_router import router as user_router


app = FastAPI()

app.include_router(product_router)
app.include_router(user_router)