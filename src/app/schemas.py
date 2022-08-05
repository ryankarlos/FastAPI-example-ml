from typing import (
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    root_validator,
)


class GetClientAge(BaseModel):
    gender: Optional[int] = None
    education: Optional[int] = None
    marriage: Optional[int] = None

    @root_validator(pre=True)
    def check_all_params_should_not_be_none(cls, values):
        gender, education, marriage = (
            values.get("gender"),
            values.get("education"),
            values.get("marriage"),
        )
        if gender is None and education is None and marriage is None:
            raise ValueError(
                "At least one of gender, education, marriage "
                "query strings must be passed with a value"
            )
        return values


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


class TrainingData(PredIn):
    default: int


class TrainingDataResponse(BaseModel):
    Response: List[TrainingData]


class PredOut(PredIn):
    prediction: dict
