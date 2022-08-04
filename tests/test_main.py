import json
from src.app.models import Payment, Client, ModelResult
from sqlmodel import select
import pytest
from decimal import Decimal
from src.app.crud import get_clients_query


def test_load_data(load, session):
    smt1 = select(Client)
    results = session.execute(smt1).fetchall()
    assert len(results) == 24000

    smt2 = select(Payment)
    results = session.execute(smt2).fetchall()
    for row in results[-1]:
        assert row.bill == 47929
        assert row.pay == 2078
    smt3 = select(ModelResult)
    results = session.execute(smt3).fetchall()
    # this table should be empty
    assert len(results) == 0

    smt4 = select(Client, Payment).join(Payment)
    results = session.execute(smt4)
    client, payment = next(results)
    assert client.gender == 2
    assert payment.pay == 0


def test_client_id(load, client):
    response = client.get("/query/clients/2")
    assert response.status_code == 200
    data = response.json()
    assert data["gender"] == 2
    assert data["education"] == 2
    assert data["marriage"] == 1
    assert data["age"] == 37


def test_payment_by_client_id(load, client):
    response = client.get("/query/payments/2")
    assert response.status_code == 200
    data = response.json()[0]
    assert data["limit"] == 50000
    assert data["repay_status"] == 0
    assert data["bill"] == 46990
    assert data["pay"] == 2000


def test_read_client_avg_age(load, client):
    response = client.get("/query/clients/age/?gender=1")
    data = response.json()
    assert data == {"average-age": 36.6}
    assert response.status_code == 200


def test_incorrect_request_path(load, client):
    response = client.get("/query/bill/payments/")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
    response = client.get("/query/clients/loyal")
    assert response.status_code == 422
    data = response.json()
    assert data['detail'][0]['msg'] == "value is not a valid integer"
    response = client.get("/query/1/clients/2")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}


def test_query_params_validation_error(load, client):
    response = client.get("/query/clients/age/?gender=male")
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "value is not a valid integer"


@pytest.mark.asyncio
async def test_avg_age_func(load, session):
    querycols1 = {'education':3, 'marriage':1}
    querycols2 = {'gender': 2,'education':1, 'marriage':2 }
    results1 = await get_clients_query(session, querycols1)
    results2 = await get_clients_query(session, querycols2)
    assert results1  == {'average-age' :Decimal('43.1')}
    assert results2 == {'average-age': Decimal('30.1')}
