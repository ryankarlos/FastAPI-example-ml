from fastapi import Depends, FastAPI, HTTPException
from .database import database, get_db
from sqlalchemy.orm import Session
from typing import List
from src.app import crud, models, schemas
from .schemas import Client, Payment, ClientIn, PaymentIn, PredIn, PredOut
import json

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


@app.get("/clients/{id}", response_model=List[Client])
async def read_clients(id: ClientIn, skip: int = 0, limit: int = 100):
    response = await crud.get_clients_query(skip=skip, limit=limit)
    return response


@app.get("/payments/{id}", response_model=List[Payment])
async def read_payments(id: PaymentIn, skip: int = 0, limit: int = 100):
    query = crud.get_clients(skip=skip, limit=limit)
    return await database.fetch_all(query)


@app.get("/train/data", response_model=List[schemas.PredOut], status_code=200)
async def get_training_data(db: Session = Depends(get_db)):
    data = crud.get_training_data(db)
    data = json.dumps(data)
    response_object = {"Response": data}
    return response_object


@app.get("/train/model", response_model=List[schemas.PredOut], status_code=200)
async def train_model(db: Session = Depends(get_db)):
    data = crud.get_training_data(db)
    response = crud.training_workflow(data)
    response_object = {"Response": response}
    return response_object


@app.get("/predict/realtime", response_model=List[PredOut], status_code=200)
async def get_prediction(payload: PredIn, db: Session = Depends(get_db)):
    response = crud.predict(payload)

    if not response:
        raise HTTPException(status_code=400, detail="Model not found.")
    response_object = crud.response_mapping(response)
    return response_object
