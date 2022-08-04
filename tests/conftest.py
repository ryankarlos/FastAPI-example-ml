import asyncio
import os
import sys
from typing import (
    Any,
    Generator,
)

from fastapi.testclient import TestClient
import pytest
from sqlmodel import (
    Session,
    SQLModel,
    create_engine,
)

from src.app.database import get_db
from src.app.main import app
from src.load_data_into_tables import async_main

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]


@pytest.fixture(scope="session")
def load():
    return asyncio.run(async_main())


@pytest.fixture()
def session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  #


@pytest.fixture(scope="function")
def client(session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client  #
    app.dependency_overrides.clear()
