from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUseCase

router = APIRouter(tags=["products"])


@router.post(path="/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUseCase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)


@router.get(path="/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUseCase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get(path="/", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def query(usecase: ProductUseCase = Depends()) -> List[ProductOut]:
    return await usecase.create()


@router.patch(path="/{id}", response_model=ProductOut, status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    Body: ProductUpdate = Body(...),
    usecase: ProductUseCase = Depends(),
) -> ProductOut:
    return await usecase.update(id=id, body=Body)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUseCase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
