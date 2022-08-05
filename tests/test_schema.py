from pydantic import ValidationError
import pytest

from src.app.schemas import GetClientAge


def test_clientage_raises_error_all_params_none():
    with pytest.raises(ValidationError) as exc_info:
        GetClientAge()
    assert exc_info.value.errors() == [
        {
            "loc": ("__root__",),
            "msg": "At least one of gender, education, marriage query strings must be passed with a value",
            "type": "value_error",
        }
    ]


def test_clientage_no_error():
    age = GetClientAge(gender=1, education=2, marriage=2)
    assert age.gender == 1
    assert age.education == 2
    assert age.marriage == 2
