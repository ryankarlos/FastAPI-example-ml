from pydantic import BaseModel
from typing import List, Union


class GetItems(BaseModel):
    id: int


class PredIn(BaseModel):
    ticker: str


class PredOut(PredIn):
    prediction: dict
