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
    repay_status_1 = Column("repay_status_1", Integer)
    repay_status_2 = Column("repay_status_2", Integer)
    repay_status_3 = Column("repay_status_3", Integer)
    repay_status_4 = Column("repay_status_4", Integer)
    repay_status_5 = Column("repay_status_5", Integer)
    repay_status_6 = Column("repay_status_6", Integer)
    bill1 = Column("bill1", Float)
    bill2 = Column("bill2", Float)
    bill3 = Column("bill3", Float)
    bill4 = Column("bill4", Float)
    bill5 = Column("bill5", Float)
    bill6 = Column("bill6", Float)
    pay1 = Column("pay1", Float)
    pay2 = Column("pay2", Float)
    pay3 = Column("pay3", Float)
    pay4 = Column("pay4", Float)
    pay5 = Column("pay5", Float)
    pay6 = Column("pay6", Float)
    default = Column("default", Integer)
    items = relationship("Client", back_populates="owner")


class ModelResult(Base):
    __tablename__ = "models"
    run_id = Column("runid", String, primary_key=True)
    version = Column("version", String)
    artifact = Column("artifact", LargeBinary)
