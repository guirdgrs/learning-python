from fastapi import APIRouter, status, Body, Path
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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from typing import Annotated 
from atleta.schemas import AtletaResumeOut
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter()

# Criar um novo atleta com método POST
@router.post(
    '/', 
    summary='Criar um novo atleta', 
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def criar_atleta(
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

    except IntegrityError as e:
        await db_session.rollback()

        cpf_duplicado = atleta_in.cpf

        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o CPF: {cpf_duplicado}"
        )
    
    result = await db_session.execute(
            select(AtletaModel)
            .options(joinedload(AtletaModel.categoria))
            .options(joinedload(AtletaModel.centro_treinamento))
            .filter(AtletaModel.id == atleta_model.id)
        )
    atleta_completo = result.scalars().first()

    return AtletaOut.model_validate(atleta_completo)

# Consultar todos os atletas com métodos GET
@router.get(
    '/', 
    summary='Consultar todos os atletas', 
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaResumeOut],
)
async def consultar_todos_atletas(
    db_session: DatabaseDependecy,
):
    query = (
    select(AtletaModel)
        .options(joinedload(AtletaModel.centro_treinamento))
        .options(joinedload(AtletaModel.categoria))
) 
    
    page = await paginate(db_session, query)

    items = [
        AtletaResumeOut(
            nome=atleta.nome,
            centro_treinamento=atleta.centro_treinamento.nome,
            categoria=atleta.categoria.nome,
        )
        for atleta in page.items
        ]

    return Page.create(items, total=page.total, params=page.params)

# Consultar atleta por ID utilizando filter by
@router.get(
    '/{id}', 
    summary='Consultar um atleta pelo ID', 
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def consultar_atleta_pelo_id(
    id: UUID4,
    db_session: DatabaseDependecy,
    
 ) -> AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no ID: {id}")
    
    return atleta

# Consultar atleta pelo nome utilizando ilike
@router.get(
    '/nome/{nome}',
    response_model=list[AtletaOut],
    summary='Consultar um atleta pelo nome',
    status_code=status.HTTP_200_OK
)
async def consultar_atleta_pelo_nome(

    nome: Annotated[str, Path(..., min_length=3, example="João Silva")],
    db_session: DatabaseDependecy,

):
    
    stmt = select(AtletaModel).where(AtletaModel.nome.ilike(f"%{nome}%"))
    result = await db_session.execute(stmt)
    atletas = result.scalars().all()

    if not atletas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta(s) não encontrado com o nome: {nome}"
        )
    
    return [AtletaOut.model_validate(atleta) for atleta in atletas]

# Consultar atleta pelo CPF utilizando filter by
@router.get(
        '/cpf/{cpf}',
        response_model=AtletaOut,
        summary='Consultar um atleta pelo CPF',
        status_code=status.HTTP_200_OK
)
async def consultar_atleta_pelo_cpf(
    db_session: DatabaseDependecy,
    cpf: str = Path(..., min_length=11, max_length=11, example="12345678900"),
):
    
    stmt = select(AtletaModel).where(AtletaModel.cpf == cpf)
    result = await db_session.execute(stmt)
    atleta = result.scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado com o CPF: {cpf}"
        )
    
    return AtletaOut.model_validate(atleta)

# Atualizar atleta pelo ID utilizando PATCH
@router.patch(
    '/{id}', 
    summary='Editar um atleta pelo ID', 
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def atualizar_atleta(
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

# Deletar atleta pelo ID utilizando DELETE
@router.delete(
    '/{id}', 
    summary='Deletar um atleta pelo ID', 
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deletar_atleta(
    id: UUID4,
    db_session: DatabaseDependecy,
    
 ) -> None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado no ID: {id}")
    
    await db_session.delete(atleta)
    await db_session.commit()