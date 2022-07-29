from fastapi import Depends, FastAPI, HTTPException
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
from src.app import crud, models, schemas

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


@app.get("/items/", response_model=List[schemas.GetItems])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/train", response_model=List[schemas.PredOut], status_code=200)
def train_model(db: Session = Depends(get_db)):
    data = crud.get_training_data(db)
    response = crud.train(data)

    if not response:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"prediction": response}
    return response_object


@app.get("/predict/realtime", response_model=List[schemas.PredOut], status_code=200)
def get_prediction(payload: schemas.PredIn, db: Session = Depends(get_db)):
    response = crud.predict(**payload)

    if not response:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"prediction": response}
    return response_object
