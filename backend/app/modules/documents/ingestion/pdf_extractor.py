"""Extract per-page text from a PDF and classify files we cannot process (T-011).

Pure function: no I/O besides its arguments, so it is easy to unit test.
"""

import re
import unicodedata
from dataclasses import dataclass

import pymupdf

MIN_AVG_CHARS_PER_PAGE = 30
_SENTENCE_END = (".", ":", ";", "!", "?", "…", '"', "”", ")")


@dataclass(frozen=True)
class ExtractedPage:
    number: int  # 1-based
    text: str


class ExtractionError(Exception):
    """code is one of: corrupted, encrypted_pdf, too_many_pages, no_text_layer."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _clean(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    lines = [ln.strip() for ln in text.splitlines()]
    out: list[str] = []
    for line in lines:
        if not line:
            if out and out[-1] != "":
                out.append("")  # keep paragraph breaks
            continue
        # Join a line broken mid-sentence: previous line has no terminal punctuation
        # and the current line starts lowercase.
        if out and out[-1] and not out[-1].endswith(_SENTENCE_END) and line[:1].islower():
            out[-1] = f"{out[-1]} {line}"
        else:
            out.append(line)
    joined = "\n".join(out).strip()
    joined = re.sub(r"[ \t]{2,}", " ", joined)
    return re.sub(r"\n{3,}", "\n\n", joined)


def extract(pdf_bytes: bytes, max_pages: int) -> list[ExtractedPage]:
    try:
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception as exc:  # PyMuPDF raises several exception types for broken files
        raise ExtractionError("corrupted") from exc

    with doc:
        if doc.needs_pass:
            raise ExtractionError("encrypted_pdf")
        if doc.page_count == 0:
            raise ExtractionError("corrupted")
        if doc.page_count > max_pages:
            raise ExtractionError("too_many_pages")
        try:
            pages = [
                ExtractedPage(number=i + 1, text=_clean(doc[i].get_text("text", sort=True)))
                for i in range(doc.page_count)
            ]
        except Exception as exc:
            raise ExtractionError("corrupted") from exc
        repaired = bool(getattr(doc, "is_repaired", False))

    total_chars = sum(len(p.text) for p in pages)
    if total_chars / len(pages) < MIN_AVG_CHARS_PER_PAGE:
        # MuPDF silently repairs truncated files; a repaired file with no readable
        # text is broken, not a scanned PDF.
        raise ExtractionError("corrupted" if repaired else "no_text_layer")
    return pages
