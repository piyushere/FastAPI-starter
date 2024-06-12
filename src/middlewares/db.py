from src.config.db import async_engine
from sqlmodel.ext.asyncio.session import AsyncSession


async def session():
    async with AsyncSession(async_engine) as session:
        yield session
