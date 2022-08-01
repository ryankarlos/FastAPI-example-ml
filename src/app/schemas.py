from pydantic import BaseModel


class PredIn(BaseModel):
    gender: int
    education: int
    marriage: int
    age: int
    limitbal: int
    repay_status: int
    bill: int
    pay: int


class PredOut(BaseModel):
    prediction: dict
