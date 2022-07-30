from pydantic import BaseModel


class ClientIn(BaseModel):
    id: int


class Client(BaseModel):
    id: int
    gender: str
    education: str
    marriage: str
    age: str


class PaymentIn(BaseModel):
    id: int


class Payment(BaseModel):
    id: int
    limitbal: int
    repay_status_1: int
    repay_status_2: int
    repay_status_3: int
    repay_status_4: int
    repay_status_5: int
    repay_status_6: int
    bill1: float
    bill2: float
    bill3: float
    bill4: float
    bill5: float
    bill6: float
    pay1: float
    pay2: float
    pay3: float
    pay4: float
    pay5: float
    pay6: float
    default: int


class PredIn(BaseModel):
    id: int
    gender: str
    education: str
    marriage: str
    age: str
    limitbal: int
    repay_status_1: int
    repay_status_2: int
    repay_status_3: int
    repay_status_4: int
    repay_status_5: int
    repay_status_6: int
    bill1: float
    bill2: float
    bill3: float
    bill4: float
    bill5: float
    bill6: float
    pay1: float
    pay2: float
    pay3: float
    pay4: float
    pay5: float
    pay6: float
    default: int


class PredOut(BaseModel):
    prediction: dict
