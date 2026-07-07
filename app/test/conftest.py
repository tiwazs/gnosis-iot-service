import pytest
import os
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from database.database import get_db

@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(os.getenv("TEST_DATABASE_URL"), pool_pre_ping=True)
    yield engine

    engine.sync_engine.dispose()

@pytest.fixture(scope="function")
async def db_session(test_engine) ->AsyncGenerator[AsyncSession, None]:
    TestingSessionMaker = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        autoflush=False
    )

    async with TestingSessionMaker() as session:
        async with session.begin():
            yield session

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = lambda: db_session

    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client

    app.dependency_overrides.clear()