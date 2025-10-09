from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class WordType(str, Enum):
    INFLECT = "Inflect"  # "활용"
    COMPOUND = "Compound"  # "복합명사"
    PREANALYSIS = "Preanalysis"  # "기분석"
    UNKNOWN = "*"  # "기타"


class MecabKoDicWord(BaseModel):
    surface: str = Field(..., description="표층형")
    pos: str = Field(..., description="품사 태그 (e.g., NNG, NNP, VV+EM+VX+EP)")
    pos_trans: str = Field(
        ...,
        description="품사 태그 번역 (e.g., 일반 명사, 고유 명사, 동사+어미+보조 용언+선어말 어미)",
    )
    semantic_class: str = Field(..., description="의미 부류 (e.g., 지명)")
    has_final_consonant: bool = Field(..., description="종성 유무")
    reading: str = Field(..., description="읽기")
    entry_type: WordType = Field(..., description="타입 (e.g., Inflected, Compound, *)")
    first_pos: str = Field(..., description="첫번째 품사 (e.g., VV)")
    last_pos: str = Field(..., description="마지막 품사 (e.g., EP)")
    expression: str = Field(
        ..., description="표현 (형태소 분해식; e.g., 해수/NNG/*+욕/NNG/*+장/NNG/*)"
    )


class ParsedExpression(BaseModel):
    lemma: str = Field(..., description="표제어")
    pos: str = Field(..., description="품사 태그 (e.g., NNG, NNP, VV)")


class Data(BaseModel):
    word: MecabKoDicWord = Field(..., description="파싱된 단어")
    parsed_expression: Optional[List[ParsedExpression]] = Field(
        None, description="형태소 분석 결과"
    )
