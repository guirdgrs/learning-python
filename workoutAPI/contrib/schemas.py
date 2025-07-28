from pydantic import BaseModel, UUID4, Field
from sqlalchemy import DateTime
from typing import Annotated

class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True

class OutMixin(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    id: Annotated[UUID4, Field(description="Identificador")]
    created_at: Annotated[DateTime, Field(description="Data de criação")]