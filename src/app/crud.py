import asyncio
import datetime
import json
import logging
import os
import pickle
import sys
import uuid

import pandas as pd
from pycaret.classification import (
    compare_models,
    finalize_model,
    predict_model,
    pull,
    save_model,
    setup,
    models,
)
from sqlalchemy import func

from src.app.models import Client, ModelResult, Payment

from .database import SessionLocal, engine

logger = logging.getLogger("api_methods")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s-%(levelname)s-[%(filename)s:%(lineno)d]-%(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

if not sys.warnoptions:
    import warnings

    warnings.simplefilter("ignore")
    os.environ["PYTHONWARNINGS"] = "ignore"  # ignore pesky sklearn warnings


def get_training_data():
    with SessionLocal.begin() as session:
        sql = session.query(Client, Payment).join(Payment).statement
    df = pd.read_sql(sql, engine)
    df = df.drop(["client_id", "id", "id_1"], axis=1)
    return df


async def query_table(schema, skip, limit):
    with SessionLocal.begin() as session:
        results = session.query(schema).offset(skip).limit(limit).all()
        session.expunge_all()  # do this so results attributes accessible outside the scope of the session
    return results


async def get_clients_query(query_cols):
    """
    eithe return single row based on client id or compute average age after
    query filter on gender, education, marriage values
    :param query_cols:
    :return:
    """
    with SessionLocal.begin() as session:
        if query_cols.get("id"):
            logger.info(
                f'Sending query to table Client, with col id={query_cols.get("id")}'
            )
            row = session.query(Client).filter(Client.id == query_cols.get("id")).one()
            response = {
                "id": row.id,
                "gender": row.gender,
                "education": row.education,
                "marriage": row.marriage,
                "age": row.age,
            }
        else:
            all_filters = []
            if query_cols.get("gender"):
                all_filters.append(Client.gender == query_cols.get("gender"))
            if query_cols.get("education"):
                all_filters.append(Client.education == query_cols.get("education"))
            if query_cols.get("marriage"):
                all_filters.append(Client.marriage == query_cols.get("marriage"))
            logger.info(
                f"Finding average client age for attributes: {str(all_filters)}"
            )
            response = session.query(func.avg(Client.age)).filter(*all_filters).scalar()
            response = {"average-age": round(response, 1)}
    return response


async def get_payments_by_client_id(id):
    with SessionLocal.begin() as session:
        logger.info(f"Sending query to table Payment, with col client id={id}")
        results = session.query(Payment).filter(Payment.client_id == id)
        response = [
            {
                "bill": row.bill,
                "pay": row.pay,
                "repay_status": row.repay_status,
                "limit": row.limitbal,
            }
            for row in results
        ]
    return response


async def get_model_artifact_from_db(version, run_id):
    with SessionLocal.begin() as session:
        if run_id is not None:
            row = session.query(ModelResult).filter(ModelResult.run_id == run_id).one()
        else:
            logger.info(
                f"Fetching latest model artifact from db for model version {version}"
            )
            row = (
                session.query(ModelResult)
                .order_by(ModelResult.created_date.desc())
                .first()
            )
        response = {"Model": row.artifact}
    return response


async def serialise_model(
    model,
    version,
    run_id,
    model_name: str,
    performance: dict,
    params: dict,
    filename="model",
):
    dirpath = os.path.dirname(os.path.dirname(__file__))
    path = f"{dirpath}/{filename}"
    save_model(model, path)
    pickle_string = pickle.dumps(model)
    params = json.dumps(params)
    with SessionLocal.begin() as session:
        session.add(
            ModelResult(
                run_id=run_id,
                name=model_name,
                parameters=params,
                auc=performance["AUC"],
                accuracy=performance["Accuracy"],
                version=version,
                artifact=pickle_string,
            )
        )
        session.commit()


async def deserialise_model(version, run_id):
    result = await get_model_artifact_from_db(version, run_id)
    pickle_string = result["Model"]
    model = pickle.loads(pickle_string)
    return model


async def create_runid():
    random_id = uuid.uuid1()
    run_id = str(str(datetime.datetime.now())) + "-" + str(random_id)
    logger.debug(f"created run-id {run_id}")
    return run_id


async def initialise_training_setup(data, target):
    setup(
        data=data,
        target=target,
        session_id=123,
        train_size=0.8,
        verbose=False,
        silent=True,
    )


async def training_workflow(data, cv_folds=5, version=0.1):
    data_copy = data.copy()
    run_id = await create_runid()
    await initialise_training_setup(data=data_copy, target="default")
    logger.info("initialised training setup")
    all_models = models()
    models_list = ",".join(all_models.reset_index()["ID"].tolist())
    logger.info(
        f"Running cv with {cv_folds} folds for models: {models_list}.Wait for completion ....."
    )
    best = compare_models(fold=cv_folds, verbose=False)
    model_name, performance = await get_model_performance_scores(best)
    logger.info(f"Performance for model {model_name}: {json.dumps(performance)}")
    await finalize_and_serialise_model(best, run_id, model_name, performance, version)
    return model_name, performance


async def get_best_model_params(model):
    params = model.named_steps.trained_model.get_params()
    return params


async def get_model_performance_scores(model):
    best_results = pull()  # fetch the model comparison results df
    logger.debug(f"CV Results Grid for all models: \n\n {best_results}")
    top_model = best_results.iloc[0, :]
    model_name = top_model["Model"]
    performance = {"AUC": top_model["AUC"], "Accuracy": top_model["Accuracy"]}
    return model_name, performance


async def finalize_and_serialise_model(
    model, run_id: str, model_name: str, performance: dict, version: float
):
    final_best = finalize_model(model, model_only=False)
    params = await get_best_model_params(final_best)
    logger.info(f"Tuned parameters for model {model_name}: \n\n {params}")
    await serialise_model(final_best, version, run_id, model_name, performance, params)
    logger.info(f"serialised model {model_name} to db with run id {run_id}")
    return final_best


async def predict(payload, version=0.1, run_id=None):
    df = pd.DataFrame([payload])
    model = await deserialise_model(version, run_id)
    predictions = predict_model(model, data=df)
    response = {"input": payload, "prediction": int(predictions["Label"][0])}
    response_mapped = response_mapping(response)
    logger.info(f"Prediction Response: {json.dumps(response_mapped)}")
    return response_mapped


def response_mapping(response):
    if response["prediction"] == 1:
        response["prediction"] = "Default"
        return response
    elif response["prediction"] == 0:
        response["prediction"] = "Not Default"
        return response


async def schedule_coroutine_tasks(*tasks):
    """
    Tasks are used to schedule coroutines concurrently.
    Wrap the coroutines into Task
    :param tasks:
    :return:
    """
    for task in asyncio.as_completed([asyncio.create_task(t) for t in tasks]):
        result = await task
        logger.info(f"Result of task: {result}")


async def gather_futures_from_coroutines(*tasks):
    """
    Passes in list of coroutines to await.gather and waits on a bunch of futures to return the
    results in the given order.
    :param tasks: List of coroutines
    :return:
    """
    results = await asyncio.gather(*tasks)
    for res in results:
        logger.debug(f"Result of task: {res}")


async def main(query_cols, payload):
    """
    Runs db sql query, model training, and prediction tasks using concurrent execution of coroutines.

    :return:
    """
    df = get_training_data()
    tasks = [
        get_clients_query(query_cols),
        get_payments_by_client_id(id=query_cols["id"]),
        training_workflow(df),
        predict(payload),
    ]
    await schedule_coroutine_tasks(*tasks)

    # alternatively can use await.gather to call futures api directly
    # await gather_futures_from_coroutines(*tasks)


if __name__ == "__main__":
    payload = {
        "gender": 2,
        "education": 2,
        "marriage": 1,
        "age": 24,
        "limitbal": 20000,
        "repay_status": 2,
        "bill": 3913,
        "pay": 698,
    }
    query_cols = {"id": 1}
    asyncio.run(main(query_cols, payload))
