import json


def test_invalid_id1(client):
    response = client.get("/query/clients/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "id not found"}


def test_invalid_id2(client):
    response = client.get("/query/payments/4")
    assert response.status_code == 404
    assert response.json()["detail"][0]["msg"] == "value is not a valid integer"
