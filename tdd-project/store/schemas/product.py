from typing import Annotated, Optional
from bson import Decimal128
from store.schemas.base import BaseSchemaMixin, OutSchema
from pydantic import AfterValidator, Field
from decimal import Decimal


class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Name of the product")
    quantity: int = Field(..., description="Quantity of the product")
    price: Decimal = Field(..., description="Price of the product")
    status: bool = Field(..., description="Status of the product")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn, OutSchema):
    ...


def convert_decimal_128(value):
    return Decimal128(str(value))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Quantity of the product")
    price: Optional[Decimal_] = Field(None, description="Price of the product")
    status: Optional[bool] = Field(None, description="Status of the product")


class ProductUpdateOut(ProductOut):
    ...
