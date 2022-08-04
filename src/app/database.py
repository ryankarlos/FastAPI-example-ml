import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
async_db_url = "postgresql+asyncpg://" + SQLALCHEMY_DATABASE_URL.split("//")[1]
async_engine = create_async_engine(
    async_db_url,
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
