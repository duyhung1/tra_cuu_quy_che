"""Domain types shared by api, modules and worker. No I/O, no framework imports."""

import uuid
from dataclasses import dataclass
from datetime import date

DOCUMENT_STATUSES = ("queued", "processing", "ready", "failed")
JOB_STATES = ("queued", "running", "retrying", "succeeded", "failed")


@dataclass(frozen=True)
class ExtractedPage:
    number: int  # 1-based
    text: str


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


@dataclass(frozen=True)
class DocMetadata:
    doc_number: str | None
    title: str | None
    effective_date: date | None


@dataclass(frozen=True)
class Job:
    id: uuid.UUID
    document_id: uuid.UUID
    attempt: int


@dataclass(frozen=True)
class RetrievedChunk:
    filename: str
    page_start: int
    content: str
    sim: float
    article: str | None = None  # "Điều 5"
    chapter: str | None = None
    doc_title: str | None = None
    doc_number: str | None = None
    effective_date: date | None = None


@dataclass(frozen=True)
class LLMResult:
    text: str
    input_tokens: int = 0
    output_tokens: int = 0


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
