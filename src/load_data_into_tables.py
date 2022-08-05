import asyncio
import uuid

from pycaret.datasets import get_data
from sqlalchemy.sql import text

from .app.database import async_engine
from .app.models import (
    Base,
    Client,
    Payment,
)


def split_data_client_payments():
    df = get_data("credit").reset_index().rename(columns={"index": "ID"})
    clients_df = df.loc[:, ["ID", "SEX", "EDUCATION", "MARRIAGE", "AGE"]]
    payments_df = df.loc[
        :, ["ID", "LIMIT_BAL", "PAY_1", "BILL_AMT1", "PAY_AMT1", "default"]
    ]
    transaction_id = payments_df.apply(lambda _: str(uuid.uuid1()), axis=1)

    payments_df.insert(0, "trans_id", transaction_id)
    clients_df.columns = [c.name for c in Client.__table__.columns]
    payments_df.columns = [c.name for c in Payment.__table__.columns]
    return payments_df, clients_df


async def async_main():
    payments_df, clients_df = split_data_client_payments()
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text("TRUNCATE TABLE clients CASCADE"))
        await conn.run_sync(_write_sql, clients_df, "clients")
        await conn.run_sync(_write_sql, payments_df, "payments")
    async with async_engine.connect() as conn:
        results = await conn.execute(text("SELECT COUNT(*) FROM payments"))
        print(f"Number of rows: {results.fetchall()[0][0]}")
    await async_engine.dispose()


def _write_sql(con, df, stmt):
    df.to_sql(stmt, con=con, if_exists="append", index=False)


if __name__ == "__main__":
    asyncio.run(async_main())
