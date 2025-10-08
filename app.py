from fastapi import FastAPI, Body, HTTPException
from utils import parse_text
from wordtypes import Data

app = FastAPI()


@app.post("/", response_model=list[Data])
def read_root(text: str = Body(..., embed=True)):

    try:
        tokens = parse_text(text)
        if not tokens:
            raise HTTPException(status_code=404, detail="Не удалось распарсить текст")
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка в данных: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка парсинга: {e}")
