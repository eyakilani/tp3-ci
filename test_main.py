from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app, get_ip

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
def test_greeting():
    response = client.get("/greeting?name=Ali")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, Ali"
    assert data["developer"] == "Dev2"
    assert "hostname" in data and "IP" in data


def test_greeting_default_name():
    assert client.get("/greeting").json()["message"] == "Hello, World"


def test_get_ip_returns_string():
    assert isinstance(get_ip(), str)


def test_get_ip_error():
    with patch("main.socket.socket") as mock_socket:
        mock_socket.return_value.connect.side_effect = OSError
        assert get_ip() == "127.0.0.1"


def test_multiply():
    response = client.post("/multiply", json={"a": 3, "b": 4})
    assert response.status_code == 200
    assert response.json()["result a*b="] == 12


def test_divide():
    response = client.post("/divide", json={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json()["result a/b="] == 5


def test_divide_by_zero():
    response = client.post("/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400


def test_remove():
    assert client.delete("/remove/1").status_code == 200
    assert client.delete("/remove/1").status_code == 404