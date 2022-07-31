from sqlalchemy import (
    Column,
    ForeignKey,
    BigInteger,
    Integer,
    String,
    LargeBinary,
    Float,
    DateTime,
)
from sqlalchemy.orm import relationship
from .database import engine, Base
from datetime import datetime


class Client(Base):
    __tablename__ = "clients"
    id = Column("id", Integer, primary_key=True)
    gender = Column("gender", Integer)
    education = Column("education", Integer)
    marriage = Column("marriage", Integer)
    age = Column("age", Integer)
    owner = relationship("Payment", back_populates="items")


class Payment(Base):
    __tablename__ = "payments"
    id = Column("id", String, primary_key=True)
    client_id = Column("client_id", ForeignKey("clients.id"))
    limitbal = Column("limitbal", BigInteger)
    repay_status = Column("repay_status", Integer)
    bill = Column("bill", Float)
    pay = Column("pay", Float)
    default = Column("default", Integer)
    items = relationship("Client", back_populates="owner")


class ModelResult(Base):
    __tablename__ = "models"
    run_id = Column("runid", String, primary_key=True)
    name = Column("name", String)
    parameters = Column("parameters", String)
    auc = Column("auc", Float)
    accuracy = Column("accuracy", Float)
    version = Column("version", Float)
    artifact = Column("artifact", LargeBinary)
    created_date = Column(DateTime, default=datetime.now)
