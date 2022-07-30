from pycaret.classification import *
import pandas as pd
from src.app.models import Client, Payment, ModelResult
from .database import SessionLocal, engine
import uuid
import datetime
import os
import asyncio
import json
import time
import pickle

session = SessionLocal()


def get_training_data():
    sql = session.query(Client, Payment).join(Payment).statement
    df = pd.read_sql(sql, engine)
    df = df.drop(["client_id", "id", "id_1"], axis=1)
    return df


async def query_table(schema, skip, limit):
    return session.query(schema).offset(skip).limit(limit).all()


async def get_clients_query(skip: int = 0, limit: int = 10):
    task = [
        {
            "gender": row.gender,
            "education": row.education,
            "marriage": row.marriage,
            "age": row.age,
        }
        for row in query_table(Client, skip, limit)
    ]
    await asyncio.gather(*task)
    return task


async def get_payments_query(skip: int = 0, limit: int = 10):
    task = [
        {"bill": row.bill1, "pay": row.pay1}
        for row in query_table(Payment, skip, limit)
    ]
    await asyncio.gather(*task)
    return task


def get_model():
    return session.query(ModelResult).all()


async def serialise_model(model, version, run_id, filename="model"):
    dirpath = os.path.dirname(os.path.dirname(__file__))
    path = f"{dirpath}/{filename}"
    save_model(model, path)
    pickle_string = pickle.dumps(model)
    session.add(ModelResult(run_id=run_id, version=version, artifact=pickle_string))


async def train(data):
    data_copy = data.copy()
    random_id = uuid.uuid1()
    run_id = str(str(datetime.datetime.now())) + "-" + str(random_id)
    setup(data=data_copy, target="default", session_id=123)
    best = compare_models(fold=5)
    await get_model_performance_scores(best)
    final_best = await finalize_and_serialise_model(best, run_id)
    return final_best


async def get_model_performance_scores(model):
    performance = predict_model(model)
    print(performance)
    return performance


async def finalize_and_serialise_model(model, run_id, version=0.1):
    final_best = finalize_model(model)
    await serialise_model(final_best, version, run_id)
    return final_best


def predict(payload):
    df = pd.DataFrame(payload)
    model = get_model()
    predictions = predict_model(model, data=df)
    response = int(predictions["Label"][0])
    return response


def response_mapping(response):
    if response == 1:
        return {"prediction": "Default"}
    elif response == 0:
        return {"prediction": "Not Default"}


async def main():
    t1 = asyncio.create_task(get_clients_query())
    t2 = asyncio.create_task(get_payments_query())
    df = get_training_data()
    t3 = asyncio.create_task(train(df))
    print("Start:", time.strftime("%X"))
    for res in asyncio.as_completed((t1, t2, t3)):
        compl = await res
    print(f'res: {compl} completed at {time.strftime("%X")}')
    print("End:", time.strftime("%X"))
    print(f"Both tasks done: {all((t1.done(), t2.done(),t3.done()))}")


if __name__ == "__main__":
    a = asyncio.run(main())
