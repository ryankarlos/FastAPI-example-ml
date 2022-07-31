import json
from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.app import crud, models, schemas

from .database import database, get_db
from .schemas import PredIn, PredOut

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Welcome from the API"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/query/clients/{id}")
async def read_client_by_id(id: int):
    query_cols = {"id": id}
    response = await crud.get_clients_query(query_cols)
    return response


@app.get("/query/clients/age/")
async def read_client_avg_age(
    gender: Union[str, None], education: Union[str, None], marriage: Union[str, None]
):
    query_cols = {"gender": gender, "education": education, "marriage": marriage}
    response = await crud.get_clients_query(query_cols)
    return response


@app.get("/query/payments/{id}")
async def read_payments_by_client_id(id: int):
    response = await crud.get_payments_by_client_id(id=id)
    return response


@app.get("/train/data/")
async def get_training_data():
    df = crud.get_training_data()
    data_dict = df.to_dict('records')
    response_object = {"Response": data_dict}
    return response_object


@app.get("/train/model/")
async def train_model(folds: int = 5, version: float = 0.1):
    data = crud.get_training_data()
    name, performance = await crud.training_workflow(data, cv_folds=folds, version=version)
    response_object = {"Response": {"Best-Model":name,
                                    "Scores": json.dumps(performance)
                                    }
                       }
    return response_object


@app.post("/predict/realtime/", status_code=200)
async def get_prediction(payload: PredIn, version: float = 0.1, run_id: Union[str, None] = None):
    payload_dict = payload.dict()
    response = await crud.predict(payload_dict, version, run_id)
    if not response:
        raise HTTPException(status_code=400, detail="Model not found.")
    return response
