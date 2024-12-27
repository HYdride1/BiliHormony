from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_post_user():
    response = client.post(
        "/users/",
        json={'name': 'first_name', 'password': '123456'}
    )
    assert response.status_code == 200
    assert response.json() == {
        "account": "user1",
        "password": "password1",
        "u_id": 0,
        "like": "",
        "coin": 100
    }


def test_get_user():
    pass
