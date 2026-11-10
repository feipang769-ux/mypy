from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from .config import get_settings
from collections.abc import Iterator
from typing import Annotated
from fastapi import Depends


def make_engine():
    settings = get_settings()
    return create_engine(
        str(settings.database_url),
        echo=True,
        pool_pre_ping=True,
    )


_engine = make_engine()
_SessionFactory = sessionmaker(_engine, expire_on_commit=False)


def get_session() -> Iterator[Session]:
    with _SessionFactory() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]        

