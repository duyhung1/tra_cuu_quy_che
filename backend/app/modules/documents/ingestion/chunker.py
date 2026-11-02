"""Article-aware chunker (T-012).

`chunk_document` (default) follows the legal structure Chương → Điều → Khoản:
- One chunk per article (Điều) when it fits in `max_tokens`; an article may span pages.
- Long articles are split on clause (Khoản) boundaries, packing clauses up to
  `target` tokens; every part repeats the article heading so it stands alone.
- A clause that is still too long is split by sentence (as `chunk_pages` does).
- Documents with no "Điều N." heading fall back to `chunk_pages`.

`chunk_pages` (fallback) is page-aware:
- A chunk never spans two pages, except that pages shorter than MIN_PAGE_TOKENS
  are merged with the following page.
- Long pages are split by paragraph, then by sentence, aiming at `target`
  tokens and never exceeding `max_tokens`; consecutive chunks of the same page
  overlap by `overlap` tokens.
"""

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from functools import lru_cache

from app.modules.documents.ingestion.legal_structure import Section, clause_units, split_sections
from app.modules.documents.ingestion.pdf_extractor import ExtractedPage

MIN_PAGE_TOKENS = 80
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?…])\s+")

TokenCounter = Callable[[str], int]


@dataclass(frozen=True)
class Chunk:
    index: int
    page_start: int
    page_end: int
    content: str
    embed_text: str
    token_count: int
    article: str | None = None  # "Điều 5"; None for the preamble or unstructured documents
    chapter: str | None = None


@lru_cache
def _bge_tokenizer():
    from tokenizers import Tokenizer

    return Tokenizer.from_pretrained("BAAI/bge-m3")


def bge_token_counter(text: str) -> int:
    return len(_bge_tokenizer().encode(text, add_special_tokens=False).ids)


def _split_units(text: str) -> list[str]:
    """Paragraphs first; paragraphs that are still long are split into sentences."""
    units: list[str] = []
    for para in (p.strip() for p in text.split("\n\n")):
        if not para:
            continue
        units.extend(s.strip() for s in _SENTENCE_SPLIT.split(para) if s.strip())
    return units


def _hard_split(unit: str, max_tokens: int, count: TokenCounter) -> list[str]:
    """Split a single over-long sentence by words."""
    words = unit.split()
    parts: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join([*current, word])
        if current and count(candidate) > max_tokens:
            parts.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        parts.append(" ".join(current))
    return parts


def _tail(text: str, overlap: int, count: TokenCounter) -> str:
    """Last ~`overlap` tokens of text, cut on a word boundary."""
    words = text.split()
    tail: list[str] = []
    for word in reversed(words):
        if count(" ".join([word, *tail])) > overlap:
            break
        tail.insert(0, word)
    return " ".join(tail)


def _merge_short_pages(pages: Sequence[ExtractedPage], count: TokenCounter) -> list[tuple[int, int, str]]:
    """Returns (page_start, page_end, text) groups; short pages join the next page."""
    groups: list[tuple[int, int, str]] = []
    pending: tuple[int, str] | None = None
    for page in pages:
        if not page.text.strip():
            continue
        start, text = (pending[0], f"{pending[1]}\n\n{page.text}") if pending else (page.number, page.text)
        if count(text) < MIN_PAGE_TOKENS and page is not pages[-1]:
            pending = (start, text)
            continue
        groups.append((start, page.number, text))
        pending = None
    if pending:
        groups.append((pending[0], pages[-1].number, pending[1]))
    return groups


def chunk_pages(
    pages: Sequence[ExtractedPage],
    filename: str,
    target: int = 500,
    max_tokens: int = 800,
    overlap: int = 75,
    count: TokenCounter = bge_token_counter,
) -> list[Chunk]:
    chunks: list[Chunk] = []

    def emit(page_start: int, page_end: int, content: str) -> None:
        content = content.strip()
        if not content:
            return
        chunks.append(
            Chunk(
                index=len(chunks),
                page_start=page_start,
                page_end=page_end,
                content=content,
                embed_text=f"{filename} — trang {page_start}: {content}",
                token_count=max(1, count(content)),
            )
        )

    for page_start, page_end, text in _merge_short_pages(pages, count):
        if count(text) <= max_tokens:
            emit(page_start, page_end, text)
            continue

        limit = max_tokens - overlap
        units: list[str] = []
        for unit in _split_units(text):
            units.extend(_hard_split(unit, limit, count) if count(unit) > limit else [unit])

        current = ""
        for unit in units:
            candidate = f"{current} {unit}".strip()
            if current and count(candidate) > target:
                emit(page_start, page_end, current)
                prefix = _tail(current, overlap, count)
                candidate = f"{prefix} {unit}".strip()
                if count(candidate) > max_tokens:
                    candidate = unit
            current = candidate
        emit(page_start, page_end, current)

    return chunks


def _split_long_unit(text: str, max_tokens: int, count: TokenCounter) -> list[str]:
    """Sentence-pack a single over-long clause into parts of at most `max_tokens`."""
    units: list[str] = []
    for unit in _split_units(text):
        units.extend(_hard_split(unit, max_tokens, count) if count(unit) > max_tokens else [unit])
    parts: list[str] = []
    current = ""
    for unit in units:
        candidate = f"{current} {unit}".strip()
        if current and count(candidate) > max_tokens:
            parts.append(current)
            candidate = unit
        current = candidate
    if current:
        parts.append(current)
    return parts


def chunk_document(
    pages: Sequence[ExtractedPage],
    filename: str,
    target: int = 500,
    max_tokens: int = 800,
    overlap: int = 75,
    count: TokenCounter = bge_token_counter,
) -> list[Chunk]:
    sections = split_sections(list(pages))
    if not any(s.article for s in sections):
        return chunk_pages(pages, filename, target, max_tokens, overlap, count)

    chunks: list[Chunk] = []

    def emit(section: Section, page_start: int, page_end: int, content: str) -> None:
        content = content.strip()
        if not content:
            return
        context = " — ".join(x for x in (filename, section.chapter) if x)
        chunks.append(
            Chunk(
                index=len(chunks),
                page_start=page_start,
                page_end=page_end,
                content=content,
                embed_text=f"{context}: {content}",
                token_count=max(1, count(content)),
                article=section.article,
                chapter=section.chapter,
            )
        )

    for section in sections:
        if count(section.text) <= max_tokens:
            emit(section, section.page_start, section.page_end, section.text)
            continue

        heading = f"{section.heading} (tiếp)" if section.article else ""
        budget = max_tokens - count(heading)
        # (page_start, page_end, text) per clause, clauses longer than the budget pre-split
        units: list[tuple[int, int, str]] = []
        for lines in clause_units(section):
            text = "\n".join(ln.text for ln in lines)
            parts = _split_long_unit(text, budget, count) if count(text) > budget else [text]
            units.extend((lines[0].page, lines[-1].page, part) for part in parts)

        current: list[tuple[int, int, str]] = []
        for unit in units:
            body = "\n".join(u[2] for u in [*current, unit])
            if current and count(body) > min(target, budget):
                emit(section, current[0][0], current[-1][1], _with_heading(current, heading, chunks, section))
                current = []
            current.append(unit)
        if current:
            emit(section, current[0][0], current[-1][1], _with_heading(current, heading, chunks, section))

    return chunks


def _with_heading(units: list[tuple[int, int, str]], heading: str, emitted: list[Chunk], section: Section) -> str:
    """The first part of an article already starts with its heading; later parts get it prepended."""
    body = "\n".join(u[2] for u in units)
    first_part = not emitted or emitted[-1].article != section.article
    return body if first_part or not heading else f"{heading}\n{body}"
