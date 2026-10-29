from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    assert client.get("/").json() == {"message": "Hello World"}

def test_addition():
    assert client.get("/addition?a=2&b=3").json() == {"result": 5}

def test_greeting():
    assert client.get("/greeting?name=Ali").json() == {"message": "Hello Ali"}