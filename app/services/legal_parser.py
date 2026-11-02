"""Chương / Điều / Khoản, metadata and amendment links (TASK-003, blueprint §6.0–6.3, §6.6)."""

import re
from datetime import date

from app.domain.text import normalize, sentences
from app.domain.types import PageText, ParsedDocument, ParsedUnit

F = re.IGNORECASE
DOC_NO = r"(\d+/[0-9A-Za-zĐđ/\-]*[0-9A-Za-zĐđ])"
ARTICLE_RE = re.compile(r"^Điều\s+(\d+[a-z]?)\s*[.:]\s*(.*)$", F)
CHAPTER_RE = re.compile(r"^Chương\s+([IVXLC]+|\d+)\b\.?\s*(.*)$", F)
CLAUSE_RE = re.compile(r"^(\d+)\.\s+")
NUMBER_RE = re.compile(r"Số\s*[:.]?\s*" + DOC_NO, F)
SIGNED_RE = re.compile(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", F)
EFFECTIVE_RES = [
    re.compile(r"hiệu lực(?:\s+thi hành)?(?:\s+kể)?\s+từ\s+ngày\s+(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})", F),
    re.compile(r"hiệu lực(?:\s+thi hành)?(?:\s+kể)?\s+từ\s+ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", F),
]
ON_SIGNING_RE = re.compile(r"hiệu lực(?:\s+thi hành)?(?:\s+kể)?\s+từ\s+ngày\s+ký", F)
TITLE_KINDS = ("QUY CHẾ", "QUYẾT ĐỊNH", "NỘI QUY", "QUY ĐỊNH", "THÔNG BÁO")
AMEND_TITLE_RE = re.compile(r"(?:sửa đổi(?:,\s*bổ sung)?|thay thế)\s+Điều\s+(\d+[a-z]?)", F)
REPLACE_CLAUSE_RE = re.compile(r"thay thế\s+khoản\s+(\d+)\s+Điều\s+(\d+[a-z]?)", F)
SO_DOC_RE = re.compile(r"số\s*" + DOC_NO, F)
INSTRUCTION_RES = [
    re.compile(r"bỏ qua\s+(?:mọi|các|tất cả)?\s*(?:quy tắc|hướng dẫn|chỉ dẫn)", F),
    re.compile(r"hãy trả lời", F),
    re.compile(r"ignore\s+(?:all|previous|the)\s+(?:rules|instructions)", F),
    re.compile(r"bất kể quy định", F),
]


def _date(d: str, m: str, y: str) -> date | None:
    try:
        return date(int(y), int(m), int(d))
    except ValueError:
        return None


def _metadata(pages: list[PageText]) -> tuple[str | None, str | None, date | None, date | None]:
    first = normalize(pages[0].text) if pages else ""
    full = normalize("\n".join(p.text for p in pages))
    number = NUMBER_RE.search(first)
    signed_m = SIGNED_RE.search(first)
    signed = _date(*signed_m.groups()) if signed_m else None
    effective = None
    for rx in EFFECTIVE_RES:  # priority by pattern, first occurrence of that pattern
        if m := rx.search(full):
            effective = _date(*m.groups())
            break
    if effective is None and ON_SIGNING_RE.search(full):
        effective = signed
    lines = [ln.strip() for ln in first.splitlines() if ln.strip()]
    title = None
    for i, ln in enumerate(lines):
        if ln.isupper() and ln.upper().startswith(TITLE_KINDS):
            title = ln
            if ln.upper() in TITLE_KINDS and i + 1 < len(lines):
                title = f"{ln} {lines[i + 1]}"
            title = title[:200]
            break
    return title, number.group(1) if number else None, signed, effective


def filter_instructions(text: str) -> tuple[str, int]:
    """Drop sentences that look like instructions (FR-012). Returns (text, dropped count)."""
    kept, dropped = [], 0
    for s in sentences(text):
        if any(rx.search(s) for rx in INSTRUCTION_RES):
            dropped += 1
        else:
            kept.append(s)
    return "".join(kept).strip(), dropped


def parse(pages: list[PageText]) -> ParsedDocument:
    title, number, signed, effective = _metadata(pages)
    articles: list[dict] = []
    chapter: str | None = None
    lines = [(p.number, normalize(ln).strip()) for p in pages for ln in p.text.splitlines() if ln.strip()]
    i = 0
    while i < len(lines):
        page, ln = lines[i]
        if m := CHAPTER_RE.match(ln):
            name, ctitle = f"Chương {m.group(1).upper()}", m.group(2).strip(" .")
            if not ctitle and i + 1 < len(lines) and lines[i + 1][1].isupper():
                i += 1
                ctitle = lines[i][1]
            chapter = f"{name}. {ctitle}" if ctitle else name
        elif m := ARTICLE_RE.match(ln):
            articles.append({"no": m.group(1), "title": m.group(2).strip(), "chapter": chapter, "page": page,
                             "clauses": [], "body": []})
        elif articles:
            art = articles[-1]
            if cm := CLAUSE_RE.match(ln):
                art["clauses"].append({"no": int(cm.group(1)), "page": page, "lines": [ln]})
            elif art["clauses"]:
                art["clauses"][-1]["lines"].append(ln)
            else:
                art["body"].append((page, ln))
        i += 1

    units: list[ParsedUnit] = []
    amendments: list[tuple[int, str, str, int | None]] = []
    filtered = 0
    full = normalize("\n".join(p.text for p in pages))
    replaced: dict[str, set[int]] = {}
    for m in REPLACE_CLAUSE_RE.finditer(full):
        replaced.setdefault(m.group(2), set()).add(int(m.group(1)))

    def add_unit(art: dict, clause_no: int, page: int, body: str) -> int | None:
        nonlocal filtered
        clean, dropped = filter_instructions(body)
        filtered += dropped
        if not clean:
            return None
        heading = f"Điều {art['no']}. {art['title']}".rstrip(". ")
        units.append(ParsedUnit(art["chapter"], art["no"], art["title"], clause_no, page, f"{heading}\n{clean}"))
        return len(units) - 1

    for art in articles:
        body_text = "\n".join(t for _, t in art["body"])
        target = AMEND_TITLE_RE.search(art["title"])
        target_doc = None
        if target:
            so = SO_DOC_RE.search(art["title"]) or SO_DOC_RE.search(body_text)
            target_doc = so.group(1) if so else None
        if art["clauses"]:
            if body_text:
                add_unit(art, 0, art["body"][0][0], body_text)
            for c in art["clauses"]:
                idx = add_unit(art, c["no"], c["page"], "\n".join(c["lines"]))
                if idx is not None and target and target_doc:
                    k = replaced.get(target.group(1), set())
                    if not k or c["no"] in k:
                        amendments.append((idx, target_doc, target.group(1), c["no"]))
        else:
            idx = add_unit(art, 0, art["page"], body_text or art["title"])
            if idx is not None and target and target_doc:
                amendments.append((idx, target_doc, target.group(1), None))

    if not articles:  # unstructured document: one unit per page
        for p in pages:
            clean, dropped = filter_instructions(normalize(p.text))
            filtered += dropped
            if clean:
                units.append(ParsedUnit(None, None, None, 0, p.number, clean))
    return ParsedDocument(title, number, signed, effective, units, amendments, filtered)
