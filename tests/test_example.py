from starlette.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_unauthenticated_user_cant_create_todos():
    todo = dict(text="run a mile", completed=False)


response = client.post("/api/todos", data=todo)
assert response.status_code == 401


def test_user_can_obtain_auth_token():
    response = client.post("/api/token", data=good_credentials)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
