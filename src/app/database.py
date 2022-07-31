import os

from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

user = os.environ["DATABASE_USER"]
password = os.environ["DATABASE_PASSWORD"]
db = "creditdata"
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@localhost/{db}"
database = Database(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
async_engine = create_async_engine(
    f"postgresql+asyncpg://{user}:{password}@localhost/{db}",
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()