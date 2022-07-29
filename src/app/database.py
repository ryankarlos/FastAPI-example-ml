from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

user = os.environ["DATABASE_USER"]
password = os.environ["DATABASE_PASSWORD"]
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@localhost/creditdata"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
