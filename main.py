"""API FastAPI du TP3 : opérations arithmétiques, salutation et gestion d'items."""
import socket

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


def get_ip():
    """Retourne l'adresse IP de l'interface réseau connectée à internet."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


@app.get("/")
def read_root():
    """Retourne un message confirmant que l'application fonctionne."""
    return {"message": "it works !"}


@app.get("/addition")
def addition(a: int, b: int):
    """Retourne la somme de a et b."""
    return {"result a+b=": a + b, "developer": "Dev1"}


@app.get("/soustraction")
def soustraction(a: int, b: int):
    """Retourne la différence de a et b."""
    return {"result a-b=": a - b, "developer": "Dev1"}


@app.get("/greeting")
def greeting(name: str = "World"):
    """Retourne un message de salutation avec le nom de la machine et son IP."""
    return {
        "message": f"Hello, {name}",
        "developer": "Dev2",
        "hostname": socket.gethostname(),
        "IP": get_ip(),
    }


class Operands(BaseModel):
    """Corps de requête contenant les deux opérandes a et b."""

    a: float
    b: float


@app.post("/multiply")
def multiply(op: Operands):
    """Retourne le produit de a et b."""
    return {"result a*b=": op.a * op.b, "developer": "Dev1"}


@app.post("/divide")
def divide(op: Operands):
    """Retourne le quotient de a par b (erreur 400 si b vaut 0)."""
    if op.b == 0:
        raise HTTPException(status_code=400, detail="Division par zéro impossible")
    return {"result a/b=": op.a / op.b, "developer": "Dev2"}


items = {1: {"name": "item1"}, 2: {"name": "item2"}}


@app.delete("/remove/{item_id}")
def remove(item_id: int):
    """Supprime l'item d'identifiant item_id (erreur 404 s'il n'existe pas)."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item introuvable")
    del items[item_id]
    return {"message": f"Item {item_id} supprimé", "developer": "Dev1"}
