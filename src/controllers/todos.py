from fastapi import APIRouter, Depends
from src.middlewares import db
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.models import Todo
todos = APIRouter()


@todos.get('/')
async def readAll(
    db_session: AsyncSession = Depends(db.session)
):
    results = await db_session.exec(select(Todo))
    return results.all()


@todos.get('/{id}')
async def read(
    id: int,
    db_session: AsyncSession = Depends(db.session)
):
    result = await db_session.get(Todo, id)
    return result


@todos.post('/')
async def create(
    todo: Todo,
    db_session: AsyncSession = Depends(db.session),
):
    db_session.add(todo)
    await db_session.commit()
    await db_session.refresh(todo)
    return todo
