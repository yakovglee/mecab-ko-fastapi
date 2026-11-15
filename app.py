import logging

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from constants import CORS_ORIGINS, MAX_TEXT_LENGTH
from utils import parse_text
from wordtypes import Data

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.post("/", response_model=list[Data])
def read_root(
    text: str = Body(..., embed=True, min_length=1, max_length=MAX_TEXT_LENGTH),
):
    try:
        tokens = parse_text(text)
    except ValueError:
        logger.exception("Invalid input for parsing")
        raise HTTPException(status_code=400, detail="Ошибка в данных")
    except Exception:
        logger.exception("Parsing failed")
        raise HTTPException(status_code=500, detail="Ошибка парсинга")
    if not tokens:
        raise HTTPException(status_code=404, detail="Не удалось распарсить текст")
    return tokens
