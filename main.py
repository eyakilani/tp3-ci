import socket
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


def get_ip():
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
    return {"message": "it works !"}


@app.get("/addition")
def addition(a: int, b: int):
    return {"result a+b=": a + b, "developer": "Dev1"}


@app.get("/greeting")
def greeting(name: str = "World"):
    return {
        "message": f"Hello, {name}",
        "developer": "Dev2",
        "hostname": socket.gethostname(),
        "IP": get_ip(),
    }

class Operands(BaseModel):
    a: float
    b: float



@app.post("/multiply")
def multiply(op: Operands):
    return {"result a*b=": op.a * op.b, "developer": "Dev1"}

@app.post("/divide")
def divide(op: Operands):
    if op.b == 0:
        raise HTTPException(status_code=400, detail="Division par zéro impossible")
    return {"result a/b=": op.a / op.b, "developer": "Dev2"}



items = {1: {"name": "item1"}, 2: {"name": "item2"}}


@app.delete("/remove/{id}")
def remove(id: int):
    if id not in items:
        raise HTTPException(status_code=404, detail="Item introuvable")
    del items[id]
    return {"message": f"Item {id} supprimé", "developer": "Dev1"}
