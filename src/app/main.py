import json
import time
from typing import (
    List,
    Union,
)

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
)
import redis
from sqlalchemy.orm import Session

from src.app import (
    crud,
    models,
)

from .database import (
    engine,
    get_db,
)
from .schemas import (
    ClientOut,
    GetClientAge,
    PaymentOut,
    PredIn,
    TrainingDataResponse,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
cache = redis.Redis(host="redis", port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.get("/")
async def index():
    count = get_hit_count()
    return {
        "message": f"Welcome to the home page of the API. "
        f"I have been visited {count} times"
    }


@app.get("/query/clients/{id}", response_model=ClientOut)
async def read_client_by_id(id: int, db: Session = Depends(get_db)):
    query_cols = {"id": id}
    response = await crud.get_clients_query(db, query_cols)
    return response


# need to add params: Model = Depends() so it is recognized as query params
# otherwise expects body in request and throws error in response
# expecting required field in body
# https://stackoverflow.com/questions/62468402/query-parameters-from-pydantic-model
@app.get("/query/clients/age/")
async def read_client_avg_age(
    params: GetClientAge = Depends(),
    db: Session = Depends(get_db),
):
    query_cols = params.dict()
    response = await crud.get_clients_query(db, query_cols)
    return response


@app.get("/query/payments/{id}", response_model=List[PaymentOut])
async def read_payments_by_client_id(id: int, db: Session = Depends(get_db)):
    response = await crud.get_payments_by_client_id(db, id=id)
    return response


@app.get("/train/data/", response_model=TrainingDataResponse)
async def get_training_data(db: Session = Depends(get_db)):
    df = crud.get_training_data(db)
    data_dict = df.to_dict("records")
    response_object = {"Response": data_dict}
    return response_object


@app.get("/train/model/")
async def train_model(
    folds: int = 5, version: float = 0.1, db: Session = Depends(get_db)
):
    data = crud.get_training_data(db)
    name, performance = await crud.training_workflow(
        data, cv_folds=folds, version=version
    )
    response_object = {
        "Response": {"Best-Model": name, "Scores": json.dumps(performance)}
    }
    return response_object


@app.post("/predict/realtime/", status_code=200)
async def get_prediction(
    payload: PredIn,
    version: float = 0.1,
    run_id: Union[str, None] = None,
    db: Session = Depends(get_db),
):
    payload_dict = payload.dict()
    response = await crud.predict(db, payload_dict, version, run_id)
    if not response:
        raise HTTPException(status_code=400, detail="Model not found.")
    return response
