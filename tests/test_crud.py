import asyncio

from pytest import approx
import sqlalchemy

from src.app.crud import main
from src.app.models import ModelResult


def test_load_main(load, session):
    payload = {
        "gender": 2,
        "education": 2,
        "marriage": 1,
        "age": 24,
        "limitbal": 20000,
        "repay_status": 2,
        "bill": 3913,
        "pay": 698,
    }
    query_cols = {"id": 1}
    asyncio.run(main(session, query_cols, payload))
    results = session.query(ModelResult).all()
    for result in results:
        assert result.name == "Linear Discriminant Analysis"
        assert result.version == 0.1
        assert result.auc == approx(0.75, rel=1e-2)
        assert result.accuracy == approx(0.82, rel=1e-2)
    truncate_query = sqlalchemy.text("TRUNCATE TABLE models")
    session.execute(truncate_query)
    session.commit()
