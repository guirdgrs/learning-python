from fastapi import APIRouter
from store.controllers.product import router as product_router

router = APIRouter()

router.include_router(product_router, prefix="/products")
