"""Vietnamese text normalisation and tokenisation (blueprint §6.0, §6.4)."""

import re
import unicodedata

_DASHES = str.maketrans({"­": "-", "‐": "-", "‑": "-", "–": "-"})
_WORD = re.compile(r"\w+", re.UNICODE)
_SENTENCE = re.compile(r"(?<!\d)[.!?;](?=\s)|\n")

STOP_WORDS = frozenset(
    "là của và thì mà bao nhiêu được có không cho các những một này đó khi nào gì ai tôi bạn "
    "hiện nay theo với về từ đến ở thế sao".split()
)


def normalize(text: str) -> str:
    return unicodedata.normalize("NFC", text).translate(_DASHES)


def words(text: str) -> list[str]:
    return _WORD.findall(normalize(text).lower())


def content_terms(text: str) -> list[str]:
    return [w for w in words(text) if w not in STOP_WORDS]


def tokenize(text: str) -> list[str]:
    """Unigrams without stop-words + bigrams built before stop-word removal (bigrams with a stop-word dropped)."""
    ws = words(text)
    uni = [w for w in ws if w not in STOP_WORDS]
    bi = [f"{a}_{b}" for a, b in zip(ws, ws[1:], strict=False) if a not in STOP_WORDS and b not in STOP_WORDS]
    return uni + bi


def sentences(text: str) -> list[str]:
    parts, last = [], 0
    for m in _SENTENCE.finditer(text):
        parts.append(text[last : m.end()])
        last = m.end()
    parts.append(text[last:])
    return [p for p in parts if p.strip()]
