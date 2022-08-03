import json
from src.app.models import Payment, Client
from src.app.crud import get_clients_query


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
    response = client.get("/query/clients/age/?id=1")
    assert response.status_code == 200
    data = response.json()


# def test_invalid_id(load, client):
#     response = client.get("/query/payments/two")
#     # assert response.status_code == 404
#     assert response.json()['detail'][0]['loc']['id'] == {}
#
