from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.app.database import Base, get_db
from src.app.main import app
from src.load_data_into_tables import async_main
from sqlmodel import Session, SQLModel, create_engine


SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]


@pytest.fixture()
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
