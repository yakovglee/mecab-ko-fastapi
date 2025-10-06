import mecab_ko as MeCab
from wordtypes import MecabKoDicWord


def parse_text(text: str) -> list[MecabKoDicWord]:
    """Парсит текст с помощью MeCab и возвращает список токенов."""

    tagger = MeCab.Tagger()
    parsed = tagger.parse(text)

    tokens: list[MecabKoDicWord] = []

    for line in parsed.splitlines():
        if line == "EOS":
            break
        surface, feature_str = line.split("\t")
        features = feature_str.split(",")

        token = MecabKoDicWord(
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

        tokens.append(token)

    return tokens
