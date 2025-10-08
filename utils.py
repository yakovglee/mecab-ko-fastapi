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
