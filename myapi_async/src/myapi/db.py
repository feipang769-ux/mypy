from .config import get_settings
from collections.abc import AsyncIterator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
     async_sessionmaker, 
     AsyncSession,
     create_async_engine
     )


def make_engine():
    settings = get_settings()
    return create_async_engine(
        str(settings.database_url),
        echo=True,
        pool_pre_ping=True,
    )


_engine = make_engine()
_SessionFactory = async_sessionmaker(_engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with _SessionFactory() as session:
            yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]        

