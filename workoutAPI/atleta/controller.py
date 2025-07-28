from fastapi import APIRouter, status, Body
from contrib.repository.dependencies import DatabaseDependecy
from atleta.schemas import AtletaIn

router = APIRouter()

@router.post(
    '/', 
    summary='Criar novo atleta', 
    status_code=status.HTTP_201_CREATED
)

async def post(
    db_session: DatabaseDependecy,
    atleta_in: AtletaIn = Body(...)
):
    pass