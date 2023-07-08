import asyncio
import os
import asyncpg
import pytest
import main

from starlette.testclient import TestClient
from typing import Generator, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.config import settings, config_db

test_engine = create_async_engine(settings.TEST_DB_URL, future=True, echo=True)

test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

CLEAN_TABLES = [
    'user',
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system("alembic revision --autogenerate -m 'test'")
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.TEST_DB_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            for table_clean in CLEAN_TABLES:
                await session.execute(f'TRUNCATE TABLE {table_clean};')


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    async def _get_test_db():
        try:
            yield test_async_session()
        finally:
            pass

    main.app.dependency_overrides[config_db.get_db] = _get_test_db()
    with TestClient(main.app) as client:
        yield client


@pytest.fixture(scope="session")
async def async_pool():
    pool = await asyncpg.create_pool()
    yield pool
    pool.close()


@pytest.fixture
async def get_user_from_database(async_pool):
    async def get_user_from_db_bu_uuid(user_id: str):
        async with async_pool.acquire() as connection:
            return await connection.fetch("SELECT * FROM user WHERE id=$1", user_id)

    return get_user_from_db_bu_uuid
