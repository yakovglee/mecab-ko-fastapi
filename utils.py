import mecab_ko as MeCab

from constants import EXPRESSION_RE, POS_SPLIT_RE, POS_TRANSLATIONS
from wordtypes import Data, MecabKoDicWord, ParsedExpression


def parse_text(text: str) -> list[Data]:
    """Парсит текст с помощью MeCab и возвращает список токенов."""
    tagger = MeCab.Tagger()

    tokens: list[Data] = []
    for line in tagger.parse(text).splitlines():
        if line == "EOS":
            break
        surface, feature_str = line.split("\t", 1)
        word = make_mecab(surface, feature_str.split(","))
        parsed = parse_expression(word.expression) if word.expression != "*" else None
        tokens.append(Data(word=word, parsed_expression=parsed))
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
    return [
        ParsedExpression(lemma=lemma, pos=pos, pos_trans=translate_pos(pos))
        for lemma, pos in EXPRESSION_RE.findall(s)
    ]


def translate_pos(pos: str) -> str:
    parts = POS_SPLIT_RE.split(pos.strip())
    return "+".join(POS_TRANSLATIONS.get(p, p) for p in parts)
