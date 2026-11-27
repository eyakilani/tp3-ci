"""Tests unitaires de l'API FastAPI."""
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app, get_ip

client = TestClient(app)


def test_root():
    """GET / retourne le message de bon fonctionnement."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "it works !"}


def test_addition():
    """GET /addition retourne la somme."""
    response = client.get("/addition?a=2&b=3")
    assert response.status_code == 200
    assert response.json()["result a+b="] == 5


def test_soustraction():
    """GET /soustraction retourne la différence."""
    response = client.get("/soustraction?a=5&b=2")
    assert response.status_code == 200
    assert response.json() == {"result a-b=": 3, "developer": "Dev1"}


def test_greeting():
    """GET /greeting retourne le message, le développeur, le hostname et l'IP."""
    response = client.get("/greeting?name=Ali")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, Ali"
    assert data["developer"] == "Dev2"
    assert "hostname" in data and "IP" in data


def test_greeting_default_name():
    """GET /greeting sans nom utilise la valeur par défaut."""
    assert client.get("/greeting").json()["message"] == "Hello, World"


def test_get_ip_returns_string():
    """get_ip retourne une chaîne de caractères."""
    assert isinstance(get_ip(), str)


def test_get_ip_error():
    """get_ip retourne 127.0.0.1 si la connexion réseau échoue."""
    with patch("main.socket.socket") as mock_socket:
        mock_socket.return_value.connect.side_effect = OSError
        assert get_ip() == "127.0.0.1"


def test_multiply():
    """POST /multiply retourne le produit."""
    response = client.post("/multiply", json={"a": 3, "b": 4})
    assert response.status_code == 200
    assert response.json()["result a*b="] == 12


def test_divide():
    """POST /divide retourne le quotient."""
    response = client.post("/divide", json={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json()["result a/b="] == 5


def test_divide_by_zero():
    """POST /divide avec b=0 retourne une erreur 400."""
    response = client.post("/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400


def test_remove():
    """DELETE /remove/{item_id} supprime l'item, puis retourne 404."""
    assert client.delete("/remove/1").status_code == 200
    assert client.delete("/remove/1").status_code == 404
