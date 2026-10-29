from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "it works !"}


def test_addition():
    response = client.get("/addition?a=2&b=3")
    assert response.status_code == 200
    assert response.json()["result a+b="] == 5


def test_soustraction():
    response = client.get("/soustraction?a=5&b=2")
    assert response.status_code == 200
    assert response.json() == {"result a-b=": 3, "developer": "Dev1"}