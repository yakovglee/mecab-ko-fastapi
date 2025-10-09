import re
import mecab_ko as MeCab
from wordtypes import Data, MecabKoDicWord, ParsedExpression


def parse_text(text: str) -> list[Data]:
    """Парсит текст с помощью MeCab и возвращает список токенов."""

    tagger = MeCab.Tagger()
    parsed = tagger.parse(text)

    tokens: list[MecabKoDicWord] = []

    for line in parsed.splitlines():
        if line == "EOS":
            break
        surface, feature_str = line.split("\t")
        features = feature_str.split(",")

        mecab_word = make_mecab(surface, features)

        if mecab_word.expression != "*":
            parsed_exp = parse_expression(mecab_word.expression)
            tokens.append(Data(word=mecab_word, parsed_expression=parsed_exp))
        else:
            tokens.append(Data(word=mecab_word))

    return tokens


def make_mecab(surface: str, features: list[str]) -> MecabKoDicWord:
    return MecabKoDicWord(
        surface=surface,
        pos=features[0],
        pos_trans=translate_pos(features[0]),
        semantic_class=features[1],
        has_final_consonant=(features[2].upper() == "T"),
        reading=features[3],
        entry_type=features[4],
        first_pos=features[5],
        last_pos=features[6],
        expression=features[7],
    )


def parse_expression(s: str) -> list[ParsedExpression]:
    pattern = re.compile(r"([^+/]+)/([A-Z]+?)/\*")

    res = []
    for lemma, pos in pattern.findall(s):
        res.append(ParsedExpression(lemma=lemma, pos=pos))

    return res


def translate_pos(pos: str) -> str:
    pos_dict = {
        "NNG": "일반 명사",
        "NNP": "고유 명사",
        "NNB": "의존 명사",
        "NNBC": "단위를 나타내는 명사",
        "NR": "수사",
        "NP": "대명사",
        "VV": "동사",
        "VA": "형용사",
        "VX": "보조 용언",
        "VCP": "긍정 지정사",
        "VCN": "부정 지정사",
        "MM": "관형사",
        "MAG": "일반 부사",
        "MAJ": "접속 부사",
        "IC": "감탄사",
        "JKS": "주격 조사",
        "JKC": "보격 조사",
        "JKG": "관형격 조사",
        "JKO": "목적격 조사",
        "JKB": "부사격 조사",
        "JKV": "호격 조사",
        "JKQ": "인용격 조사",
        "JX": "보조사",
        "JC": "접속 조사",
        "EP": "선어말 어미",
        "EF": "종결 어미",
        "EC": "연결 어미",
        "ETN": "명사형 전성 어미",
        "ETM": "관형형 전성 어미 ",
        "XPN": "체언 접두사",
        "XSN": "명사 파생 접미사",
        "XSV": "동사 파생 접미사",
        "XSA": "형용사 파생 접미사",
        "XR": "어근",
        "SF": "마침표, 물음표, 느낌표",
        "SE": "줄임표",
        "SSO": "여는 괄호",
        "SSC": "닫는 괄호",
        "SC": "구분자",
        "SY": "SY",
        "SL": "외국어",
        "SH": "한자",
        "SN": "숫자",
    }

    return pos_dict.get(pos, pos)
