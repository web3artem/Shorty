import os
from httpx import AsyncClient, ASGITransport

import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.core.config import settings
from app.db.models import Base
from app.db.session import get_db

from main import app

# async engine for interacting with DB
test_sync_engine = create_engine(settings.TEST_SYNC_DATABASE_URL)


# async session for interacting with DB


@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True)
        test_async_session = async_sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        ...


@pytest.fixture(scope="function")
async def client():
    # change prod DB to test DB
    app.dependency_overrides[get_db] = _get_test_db

    async with AsyncClient(transport=ASGITransport(app=app)) as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def prepare_database():
    Base.metadata.drop_all(test_sync_engine)
    Base.metadata.create_all(test_sync_engine)
