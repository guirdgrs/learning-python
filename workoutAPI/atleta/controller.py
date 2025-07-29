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
from atleta.schemas import AtletaUpdate
from fastapi import HTTPException

from sqlalchemy.orm import joinedload

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
    try:
        atleta_model = AtletaModel(
            id=uuid4(),
            created_at=datetime.now(),
            **atleta_in.model_dump(exclude={'categoria', 'centro_treinamento'})
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

        result = await db_session.execute(
            select(AtletaModel)
            .options(joinedload(AtletaModel.categoria))
            .options(joinedload(AtletaModel.centro_treinamento))
            .filter(AtletaModel.id == atleta_model.id)
        )
        atleta_completo = result.scalars().first()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir os dados no banco"
        )

    return AtletaOut.model_validate(atleta_completo)

@router.get(
    '/', 
    summary='Consultar todos os atletas', 
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)

async def query(
    db_session: DatabaseDependecy,
    
 ) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
    return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.get(
    '/{id}', 
    summary='Consultar um atleta pelo ID', 
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)

async def query(
    id: UUID4,
    db_session: DatabaseDependecy,
    
 ) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no ID: {id}")
    
    return atleta

@router.patch(
    '/{id}', 
    summary='Editar um atleta pelo ID', 
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)

async def query(
    id: UUID4,
    db_session: DatabaseDependecy,
    atleta_up: AtletaUpdate = Body(...)

 ) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no ID: {id}")
    
    atleta_up = atleta_up.model_dump(exclude_unset=True)

    for key, value in atleta_up.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta

@router.delete(
    '/{id}', 
    summary='Deletar um atleta pelo ID', 
    status_code=status.HTTP_204_NO_CONTENT,
)

async def query(
    id: UUID4,
    db_session: DatabaseDependecy,
    
 ) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no ID: {id}")
    
    await db_session.delete(atleta)
    await db_session.commit()
