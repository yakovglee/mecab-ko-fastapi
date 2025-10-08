# mecab-ko-fastapi

FastAPI service for **Korean morphological analysis** powered by **MeCab‑ko** and **mecab-ko-dic**.

---

## ✨ Features

* Simple HTTP API for analyzing Korean text.
* Returns tokens with POS tags, semantic info, and (if available) detailed morpheme breakdown.
* Interactive Swagger documentation available at `/docs`.

---

## 📦 Requirements

* Python 3.10+
* OS supporting MeCab binaries (Linux/macOS/WSL recommended)

> Python dependencies are listed in `requirements.txt`.

---

## 🚀 Installation & Run

```bash
# 1) Clone the repository
git clone https://github.com/yakovglee/mecab-ko-fastapi.git
cd mecab-ko-fastapi

# 2) (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run the development server
fastapi dev app.py
# Default: http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
```

---

## 🔌 API

### POST `/`

Endpoint for morphological analysis.

**Request Body (JSON):**

```json
{
  "text": "안녕하세요 저는 학생입니다."
}
```

**Successful Response (`200 OK`, JSON):**
Returns a **list** of `Data` objects.

```json
[
  {
    "word": {
      "surface": "안녕",
      "pos": "NNG",
      "semantic_class": "*",
      "has_final_consonant": true,
      "reading": "안녕",
      "entry_type": "*",
      "first_pos": "*",
      "last_pos": "*",
      "expression": "*"
    },
    "parsed_expression": null
  },
  {
    "word": {
      "surface": "하",
      "pos": "XSV",
      "semantic_class": "*",
      "has_final_consonant": false,
      "reading": "하",
      "entry_type": "*",
      "first_pos": "*",
      "last_pos": "*",
      "expression": "*"
    },
    "parsed_expression": null
  },
  {
    "word": {
      "surface": "세요",
      "pos": "EP+EF",
      "semantic_class": "*",
      "has_final_consonant": false,
      "reading": "세요",
      "entry_type": "Inflect",
      "first_pos": "EP",
      "last_pos": "EF",
      "expression": "시/EP/*+어요/EF/*"
    },
    "parsed_expression": [
      {
        "lemma": "시",
        "pos": "EP"
      },
      {
        "lemma": "어요",
        "pos": "EF"
      }
    ]
  },
  {
    "word": {
      "surface": "저",
      "pos": "NP",
      "semantic_class": "*",
      "has_final_consonant": false,
      "reading": "저",
      "entry_type": "*",
      "first_pos": "*",
      "last_pos": "*",
      "expression": "*"
    },
    "parsed_expression": null
  },
  {
    "word": {
      "surface": "는",
      "pos": "JX",
      "semantic_class": "*",
      "has_final_consonant": true,
      "reading": "는",
      "entry_type": "*",
      "first_pos": "*",
      "last_pos": "*",
      "expression": "*"
    },
    "parsed_expression": null
  },
  {
    "word": {
      "surface": "학생",
      "pos": "NNG",
      "semantic_class": "*",
      "has_final_consonant": true,
      "reading": "학생",
      "entry_type": "*",
      "first_pos": "*",
      "last_pos": "*",
      "expression": "*"
    },
    "parsed_expression": null
  },
  {
    "word": {
      "surface": "입니다",
      "pos": "VCP+EF",
      "semantic_class": "*",
      "has_final_consonant": false,
      "reading": "입니다",
      "entry_type": "Inflect",
      "first_pos": "VCP",
      "last_pos": "EF",
      "expression": "이/VCP/*+ᄇ니다/EF/*"
    },
    "parsed_expression": [
      {
        "lemma": "이",
        "pos": "VCP"
      },
      {
        "lemma": "ᄇ니다",
        "pos": "EF"
      }
    ]
  },
  {
    "word": {
      "surface": ".",
      "pos": "SF",
      "semantic_class": "*",
      "has_final_consonant": false,
      "reading": "*",
      "entry_type": "*",
      "first_pos": "*",
      "last_pos": "*",
      "expression": "*"
    },
    "parsed_expression": null
  }
]
```

---

## 🧠 Data Models

### `MecabKoDicWord`

* `surface`: string — surface form
* `pos`: string — POS tags (e.g., `NNG`, `VV+EP`)
* `semantic_class`: string — semantic class (e.g., *지명*)
* `has_final_consonant`: bool — indicates presence of final consonant (종성)
* `reading`: string — reading
* `entry_type`: enum — entry type (`Inflect`, `Compound`, `Preanalysis`, `*`)
* `first_pos`: string — first POS
* `last_pos`: string — last POS
* `expression`: string — morpheme decomposition (e.g., `해수/NNG/*+욕/NNG/*+장/NNG/*`)

### `ParsedExpression`

* `lemma`: string — lemma
* `pos`: string — POS tag

### `Data`

* `word`: `MecabKoDicWord`
* `parsed_expression`: `List[ParsedExpression] | null`

> Full POS tag list available in “Tags & Dictionary v2” (see links below).

---

## 📚 References

* Python binding: [GitHub](https://github.com/NoUnique/pymecab-ko)
* MeCab‑ko: [GitHub](https://github.com/hephaex/mecab-ko)
* POS Tags & Dictionary: [Google Sheets](https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY/edit?gid=589544265#gid=589544265)

---

## 🔧 Development Notes

Project structure overview:

* `app.py` — FastAPI app and `/` endpoint.
* `utils.py` — calls `mecab_ko.Tagger()`, converts MeCab output into Pydantic models, parses expressions using regex `([^+/]+)/([A-Z]+?)/\*`.
* `wordtypes.py` — Pydantic models and POS/type enumerations.

Run formatter before committing:

```bash
black .
```

---

## 📝 License

Distributed under the **GPL‑2.0** License. See `LICENSE` for details.
