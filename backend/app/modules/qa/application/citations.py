"""Turn the [n] markers of an answer into a list of sources (T-020).

The model cites retrieved excerpts by number; only numbers that exist are kept,
so a hallucinated "[9]" never becomes a fake source.
"""

import re
from dataclasses import dataclass
from datetime import date

from app.modules.qa.ports import RetrievedChunk

_MARKER_RE = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")


@dataclass(frozen=True)
class Source:
    ref: int  # the n in [n], 1-based
    filename: str
    page: int
    article: str | None
    chapter: str | None
    doc_title: str | None
    doc_number: str | None
    effective_date: date | None

    def as_dict(self) -> dict:
        return {
            "ref": self.ref,
            "filename": self.filename,
            "page": self.page,
            "article": self.article,
            "chapter": self.chapter,
            "doc_title": self.doc_title,
            "doc_number": self.doc_number,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
        }


def cited_refs(answer: str, n_chunks: int) -> list[int]:
    """Distinct cited numbers in order of first appearance, limited to 1..n_chunks."""
    refs: list[int] = []
    for m in _MARKER_RE.finditer(answer):
        for part in m.group(1).split(","):
            ref = int(part)
            if 1 <= ref <= n_chunks and ref not in refs:
                refs.append(ref)
    return refs


def strip_invalid_markers(answer: str, n_chunks: int) -> str:
    """Remove markers that point to no excerpt, e.g. "[9]" when only 5 were sent."""

    def fix(m: re.Match[str]) -> str:
        valid = [p.strip() for p in m.group(2).split(",") if 1 <= int(p) <= n_chunks]
        return f"{m.group(1)}[{', '.join(valid)}]" if valid else ""

    return re.sub(r"(\s*)" + _MARKER_RE.pattern, fix, answer).strip()


def build_sources(answer: str, chunks: list[RetrievedChunk]) -> list[Source]:
    sources = []
    for ref in cited_refs(answer, len(chunks)):
        ch = chunks[ref - 1]
        sources.append(
            Source(
                ref=ref,
                filename=ch.filename,
                page=ch.page_start,
                article=ch.article,
                chapter=ch.chapter,
                doc_title=ch.doc_title,
                doc_number=ch.doc_number,
                effective_date=ch.effective_date,
            )
        )
    return sources
