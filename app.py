from fastapi import FastAPI, Body
from utils import parse_text

app = FastAPI()


@app.post("/")
def read_root(text: str = Body(..., embed=True)):
    return parse_text(text)
