from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class WordType(str, Enum):
    INFLECT = "Inflect"  # "활용"
    COMPOUND = "Compound"  # "복합명사"
    PREANALYSIS = "Preanalysis"  # "기분석"
    UNKNOWN = "*"  # "기타"


class POSTag(Enum):
    # 체언
    NNG = "일반 명사"  # 일반 명사
    NNP = "고유 명사"  # 고유 명사
    NNB = "의존 명사"  # 의존 명사
    NNBC = "단위를 나타내는 명사"  # 단위를 나타내는 명사

    NR = "수사"  # 수사
    NP = "대명사"  # 대명사

    # 용언
    VV = "동사"  # 동사
    VA = "형용사"  # 형용사
    VX = "보조 용언"  # 보조 용언
    VCP = "긍정 지정사"  # 긍정 지정사
    VCN = "부정 지정사"  # 부정 지정사

    # 수식언
    MM = "관형사"  # 관형사
    MAG = "일반 부사"  # 일반 부사
    MAJ = "접속 부사"  # 접속 부사

    # 독립언
    IC = "감탄사"  # 감탄사

    # 관계언 (조사)
    JKS = "주격 조사"  # 주격 조사
    JKC = "보격 조사"  # 보격 조사
    JKG = "관형격 조사"  # 관형격 조사
    JKO = "목적격 조사"  # 목적격 조사
    JKB = "부사격 조사"  # 부사격 조사
    JKV = "호격 조사"  # 호격 조사
    JKQ = "인용격 조사"  # 인용격 조사
    JX = "보조사"  # 보조사
    JC = "접속 조사"  # 접속 조사

    # 어미
    EP = "선어말 어미"  # 선어말 어미
    EF = "종결 어미"  # 종결 어미
    EC = "연결 어미"  # 연결 어미
    ETN = "명사형 전성 어미"  # 명사형 전성 어미
    ETM = "관형형 전성 어미 "  # 관형형 전성 어미

    # 접사/어근
    XPN = "체언 접두사"  # 체언 접두사
    XSN = "명사 파생 접미사"  # 명사 파생 접미사
    XSV = "동사 파생 접미사"  # 동사 파생 접미사
    XSA = "형용사 파생 접미사"  # 형용사 파생 접미사
    XR = "어근"  # 어근

    # 기호
    SF = "마침표, 물음표, 느낌표"  # 마침표/물음표/느낌표
    SE = "줄임표"  # 줄임표
    SSO = "여는 괄호"  # 여는 괄호 (, [
    SSC = "닫는 괄호"  # 닫는 괄호 ), ]
    SC = "구분자"  # 구분자 , · / :
    SY = "SY"  # 기타 부호(붙임표 등 포함)

    # 한글 이외
    SL = "외국어"  # 외국어
    SH = "한자"  # 한자
    SN = "숫자"  # 숫자


class MecabKoDicWord(BaseModel):
    surface: str = Field(..., description="표층형")
    pos: str = Field(..., description="품사 태그 (e.g., NNG, NNP, VV+EM+VX+EP)")
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
