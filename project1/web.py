from model import Creature
from fastapi import FastAPI

app = FastAPI()

@app.get('/creature')
def getP_all() -> list[Creature]:
    from data import get_creatures
    return get_creatures()