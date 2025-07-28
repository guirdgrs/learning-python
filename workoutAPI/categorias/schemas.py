from typing_extensions import Annotated
from contrib.schemas import BaseSchema
from pydantic import Field, UUID4

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Scale", max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description="Identificador da categoria")]