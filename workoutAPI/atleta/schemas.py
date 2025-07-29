from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from contrib.schemas import BaseSchema, OutMixin
from categorias.schemas import CategoriaIn
from centro_treinamento.schemas import CentroTreinamentoAtleta

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="João da Silva", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="12345678900", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=25)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kg", example=70.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", example=1.75)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M/F", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(description="Nome do atleta", example="João da Silva", max_length=50)] | None = None
    cpf: Annotated[Optional[str], Field(description="CPF do atleta", example="12345678900", max_length=11)] | None = None
    idade: Annotated[Optional[int], Field(description="Idade do atleta", example=25)] | None = None