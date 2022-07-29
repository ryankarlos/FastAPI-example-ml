from pycaret.datasets import get_data
from sqlalchemy.sql import text
from .app.database import engine
from .app.models import clients, payments

df = get_data("credit").reset_index().rename(columns={"index": "ID"})
clients_df = df.loc[:, ["ID", "SEX", "EDUCATION", "MARRIAGE", "AGE"]]
payments_df = df.drop(["SEX", "EDUCATION", "MARRIAGE", "AGE"], axis=1)

clients_df.columns = clients.columns.keys()
payments_df.columns = payments.columns.keys()

with engine.connect() as conn:
    with conn.begin():
        conn.execute(text(f"TRUNCATE TABLE clients CASCADE"))
        clients_df.to_sql("clients", con=conn, if_exists="append", index=False)
        payments_df.to_sql("payments", con=conn, if_exists="append", index=False)
        results = conn.execute(text(f"SELECT COUNT(*) FROM payments")).fetchall()
        print(f"Number of rows: {results[0][0]}")
