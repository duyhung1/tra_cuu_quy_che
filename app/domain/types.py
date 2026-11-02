"""Domain types (blueprint §3). No I/O, no framework imports."""

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class PageText:
    number: int  # 1-based
    text: str


@dataclass
class Document:
    id: int
    filename: str
    title: str | None
    doc_number: str | None
    effective_date: date | None
    signed_date: date | None
    pages: int | None
    status: str  # processing | ready | failed
    error_code: str | None = None
    units_filtered: int = 0

    @property
    def eff(self) -> date:
        """Date used to compare documents (blueprint §6.2). date.min = unknown."""
        return self.effective_date or self.signed_date or date.min

    @property
    def eff_unknown(self) -> bool:
        return self.effective_date is None and self.signed_date is None


@dataclass
class Unit:
    id: int
    document_id: int
    chapter: str | None
    article_no: str | None
    article_title: str | None
    clause_no: int  # 0 = whole article (or page unit when article_no is None)
    page: int
    text: str  # starts with the article heading line

    @property
    def body(self) -> str:
        """Text without the heading line."""
        if self.article_no and "\n" in self.text:
            return self.text.split("\n", 1)[1].strip()
        return self.text.strip()


@dataclass(frozen=True)
class Amendment:
    source_unit_id: int
    target_doc_number: str
    target_article_no: str
    target_clause_no: int | None  # None = whole article


@dataclass(frozen=True)
class Hit:
    unit: Unit
    score: float


@dataclass
class Resolution:
    primary: Unit | None
    superseded: list[Unit] = field(default_factory=list)
    upcoming: list[Unit] = field(default_factory=list)
    found_score: float = 0.0
    coverage: float = 0.0
    matched_terms: int = 0
    not_found: bool = False


@dataclass(frozen=True)
class Source:
    ref: int
    filename: str
    doc_title: str | None
    doc_number: str | None
    effective_date: date | None
    article: str | None  # "Điều 5"
    clause: str | None  # "khoản 1"
    page: int

    def as_dict(self) -> dict:
        return {
            "ref": self.ref,
            "filename": self.filename,
            "doc_title": self.doc_title,
            "doc_number": self.doc_number,
            "effective_date": self.effective_date.isoformat() if self.effective_date else None,
            "article": self.article,
            "clause": self.clause,
            "page": self.page,
        }


@dataclass(frozen=True)
class Answer:
    text: str
    found: bool
    sources: list[Source]


@dataclass(frozen=True)
class UsageRecord:
    latency_ms: int
    status: str  # ok | error
    cited_count: int


@dataclass(frozen=True)
class IngestResult:
    filename: str
    status: str  # ready | failed
    document_id: int | None = None
    error_code: str | None = None
    message: str | None = None

    def as_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class ParsedUnit:
    chapter: str | None
    article_no: str | None
    article_title: str | None
    clause_no: int
    page: int
    text: str


@dataclass
class ParsedDocument:
    title: str | None
    doc_number: str | None
    signed_date: date | None
    effective_date: date | None
    units: list[ParsedUnit]
    # (index into units, target doc number, target article, target clause or None)
    amendments: list[tuple[int, str, str, int | None]]
    filtered: int = 0
