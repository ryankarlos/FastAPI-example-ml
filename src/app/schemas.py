from pydantic import BaseModel

from typing import Optional


class GetClientAge(BaseModel):
    gender: Optional[int] = None
    education: Optional[int] = None
    marriage: Optional[int] = None


class ClientOut(BaseModel):
    gender: int
    education: int
    marriage: int
    age: int


class PaymentOut(BaseModel):
    limit: int
    repay_status: int
    bill: int
    pay: int


class PredIn(BaseModel):
    gender: int
    education: int
    marriage: int
    age: int
    limitbal: int
    repay_status: int
    bill: int
    pay: int


class PredOut(PredIn):
    prediction: dict
