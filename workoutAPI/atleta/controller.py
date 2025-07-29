from fastapi import APIRouter, status, Body
from contrib.repository.dependencies import DatabaseDependecy
from atleta.schemas import AtletaIn, AtletaOut
from atleta.models import AtletaModel
from pydantic import UUID4
from uuid import uuid4
from datetime import datetime
from sqlalchemy.future import select

from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTreinamentoModel

from fastapi import HTTPException

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo atleta', 
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)

async def post(
    db_session: DatabaseDependecy,
    atleta_in: AtletaIn = Body(...)
):

    categoria_name = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_name))
        ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria não encontrada: {categoria_name}"
        )
    
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
        ).scalars().first() 

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria não encontrada: {centro_treinamento_nome}"
        )

    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
    
    atleta_model.categoria_id = categoria.pk_id
    atleta_model.centro_treinamento_id = centro_treinamento.pk_id

    db_session.add(atleta_model)
    await db_session.commit()
    await db_session.refresh(atleta_model)

    return atleta_model