from typing import Optional
from store.schemas.base import BaseSchemaMixin
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., description="Name of the product")
    quantity: int = Field(..., description="Quantity of the product")
    price: float = Field(..., description="Price of the product")
    status: bool = Field(..., description="Status of the product")


class ProductIn(BaseSchemaMixin, ProductBase):
    ...


class ProductOut(ProductIn):
    ...


class ProductUpdate(ProductBase):
    quantity: Optional[int] = Field(None, description="Quantity of the product")
    price: Optional[float] = Field(None, description="Price of the product")
    status: Optional[bool] = Field(None, description="Status of the product")


class ProductUpdateOut(ProductUpdate):
    ...
