from sqlalchemy import (
    MetaData,
    Table,
    Column,
    ForeignKey,
    BigInteger,
    Integer,
    String,
    LargeBinary,
    Float,
    DateTime,
)
from .database import engine
from datetime import datetime

metadata = MetaData()


clients = Table(
    "clients",
    metadata,
    Column("id", Integer(), primary_key=True),
    Column("gender", String()),
    Column("education", String()),
    Column("marriage", String()),
    Column("age", Integer()),
)


payments = Table(
    "payments",
    metadata,
    Column("client_id", ForeignKey("clients.id")),
    Column("limitbal", BigInteger()),
    Column("repay_status_1", Integer()),
    Column("repay_status_2", Integer()),
    Column("repay_status_3", Integer()),
    Column("repay_status_4", Integer()),
    Column("repay_status_5", Integer()),
    Column("repay_status_6", Integer()),
    Column("bill1", Float()),
    Column("bill2", Float()),
    Column("bill3", Float()),
    Column("bill4", Float()),
    Column("bill5", Float()),
    Column("bill6", Float()),
    Column("pay1", Float()),
    Column("pay2", Float()),
    Column("pay3", Float()),
    Column("pay4", Float()),
    Column("pay5", Float()),
    Column("pay6", Float()),
    Column("default", Integer()),
)


model_results = Table(
    "models",
    metadata,
    Column("run_id", Integer(), primary_key=True),
    Column("model", String(50), nullable=False),
    Column("performance", String(255), nullable=False),
    Column("version", Float(), nullable=False),
    Column("artifact", LargeBinary(), nullable=False),
)

if __name__ == "__main__":
    metadata.create_all(engine)
