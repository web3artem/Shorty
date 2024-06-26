from typing import Generator

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


def new_async_engine(uri: URL) -> AsyncEngine:
    return create_async_engine(uri, future=True, echo=False)


# create async engine for interaction with db
_ASYNC_ENGINE = new_async_engine(settings.DATABASE_URL)

# create session for interacting with db
_ASYNC_SESSIONMAKER = async_sessionmaker(_ASYNC_ENGINE, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = _ASYNC_SESSIONMAKER()
        yield session
    finally:
        await session.close()
