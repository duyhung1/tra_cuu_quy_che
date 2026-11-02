"""Structure and metadata of Vietnamese regulation documents (T-012).

Splits extracted pages into sections Chương → Điều, and detects the document's
number (số hiệu), title and effective date. Pure functions: easy to unit test.
"""

import re
from dataclasses import dataclass, field
from datetime import date

from app.domain import DocMetadata, ExtractedPage

# "Điều 5. Công tác phí" / "Điều 12a: ..." — the number must be followed by "." or ":"
# so references inside a sentence ("theo Điều 5 của Quy chế") are not headings.
ARTICLE_RE = re.compile(r"^Điều\s+(\d+[a-z]?)\s*[.:]\s*(.*)$")
CHAPTER_RE = re.compile(r"^Chương\s+([IVXLC]+|\d+)\b\.?\s*(.*)$", re.IGNORECASE)
CLAUSE_RE = re.compile(r"^\d+\.\s")

_DOC_NUMBER_RE = re.compile(r"Số\s*[:.]?\s*(\d+[/\-][0-9A-Za-zĐđ/\-]+)")
_EFFECTIVE_RE = re.compile(
    r"hiệu lực(?: thi hành)?(?: kể)? từ ngày\s+(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})", re.IGNORECASE
)
_EFFECTIVE_ON_SIGNING_RE = re.compile(r"hiệu lực(?: thi hành)?(?: kể)? từ ngày ký", re.IGNORECASE)
_SIGNED_RE = re.compile(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", re.IGNORECASE)
_TITLE_KINDS = ("QUY CHẾ", "QUYẾT ĐỊNH", "NỘI QUY", "QUY ĐỊNH", "THÔNG TƯ", "NGHỊ ĐỊNH", "LUẬT", "HƯỚNG DẪN")
TITLE_MAX_CHARS = 200
# PDF fonts often encode "-" as a soft hyphen or a Unicode dash (e.g. "QC\u00adSM")
_DASHES = str.maketrans({"\u00ad": "-", "\u2010": "-", "\u2011": "-", "\u2013": "-"})


@dataclass(frozen=True)
class Line:
    page: int
    text: str


@dataclass
class Section:
    """One article (Điều), or the preamble before the first article (article=None)."""

    article: str | None  # "Điều 5"
    title: str  # "Công tác phí"
    chapter: str | None  # "Chương II. CHẾ ĐỘ CÔNG TÁC PHÍ"
    lines: list[Line] = field(default_factory=list)

    @property
    def heading(self) -> str:
        return f"{self.article}. {self.title}".rstrip(". ") if self.article else ""

    @property
    def text(self) -> str:
        return "\n".join(ln.text for ln in self.lines)

    @property
    def page_start(self) -> int:
        return self.lines[0].page

    @property
    def page_end(self) -> int:
        return self.lines[-1].page


def _lines(pages: list[ExtractedPage]) -> list[Line]:
    return [Line(p.number, ln.strip()) for p in pages for ln in p.text.splitlines() if ln.strip()]


def split_sections(pages: list[ExtractedPage]) -> list[Section]:
    """Chapter headings are not part of any article text; they label the articles after them."""
    sections: list[Section] = []
    chapter: str | None = None
    current = Section(article=None, title="", chapter=None)
    lines = _lines(pages)
    i = 0
    while i < len(lines):
        line = lines[i]
        if m := CHAPTER_RE.match(line.text):
            name, title = f"Chương {m.group(1).upper()}", m.group(2).strip(" .")
            # Chapter title on its own line, e.g. "Chương II" / "CHẾ ĐỘ CÔNG TÁC PHÍ"
            if not title and i + 1 < len(lines) and lines[i + 1].text.isupper():
                i += 1
                title = lines[i].text
            chapter = f"{name}. {title}" if title else name
        elif m := ARTICLE_RE.match(line.text):
            if current.lines:
                sections.append(current)
            current = Section(article=f"Điều {m.group(1)}", title=m.group(2).strip(), chapter=chapter)
            current.lines.append(line)
        else:
            current.lines.append(line)
        i += 1
    if current.lines:
        sections.append(current)
    return sections


def clause_units(section: Section) -> list[list[Line]]:
    """Group an article's lines by clause (Khoản: lines starting "1.", "2."...).
    The heading line stays with the first clause."""
    units: list[list[Line]] = []
    for line in section.lines:
        joins_heading = section.article is not None and len(units) == 1 and len(units[0]) == 1
        if not units or (CLAUSE_RE.match(line.text) and not joins_heading):
            units.append([line])
        else:
            units[-1].append(line)
    return units


def _date(d: str, m: str, y: str) -> date | None:
    try:
        return date(int(y), int(m), int(d))
    except ValueError:
        return None


def _title(first_page: list[str]) -> str | None:
    for i, line in enumerate(first_page):
        if line.upper().startswith(_TITLE_KINDS) and line.isupper():
            title = line
            # "QUYẾT ĐỊNH" / "Về việc ..." or "QUY CHẾ" / "CHI TIÊU NỘI BỘ"
            if line.upper() in _TITLE_KINDS and i + 1 < len(first_page):
                title = f"{line} {first_page[i + 1]}"
            return title[:TITLE_MAX_CHARS]
    return None


def detect_metadata(pages: list[ExtractedPage]) -> DocMetadata:
    if not pages:
        return DocMetadata(None, None, None)
    first = [ln.strip().translate(_DASHES) for ln in pages[0].text.splitlines() if ln.strip()]
    first_text = "\n".join(first)
    full_text = "\n".join(p.text for p in pages)

    number = _DOC_NUMBER_RE.search(first_text)
    effective: date | None = None
    if m := _EFFECTIVE_RE.search(full_text):
        effective = _date(*m.groups())
    elif _EFFECTIVE_ON_SIGNING_RE.search(full_text) and (s := _SIGNED_RE.search(first_text)):
        effective = _date(*s.groups())
    return DocMetadata(
        doc_number=number.group(1) if number else None,
        title=_title(first),
        effective_date=effective,
    )
