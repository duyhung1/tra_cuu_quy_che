"""PdfExtractor adapter on PyMuPDF (TASK-004, SAD §3.2 step 4)."""

import pymupdf

from app.domain.errors import AppError
from app.domain.types import PageText

MIN_AVG_CHARS_PER_PAGE = 30


class PyMuPdfExtractor:
    def extract(self, data: bytes, max_pages: int) -> list[PageText]:
        try:
            doc = pymupdf.open(stream=data, filetype="pdf")
        except Exception as exc:  # PyMuPDF raises several types for broken files
            raise AppError("corrupted") from exc
        with doc:
            if doc.needs_pass:
                raise AppError("encrypted_pdf")
            if doc.page_count == 0:
                raise AppError("corrupted")
            if doc.page_count > max_pages:
                raise AppError("too_many_pages")
            try:
                pages = [PageText(i + 1, doc[i].get_text("text", sort=True)) for i in range(doc.page_count)]
            except Exception as exc:
                raise AppError("corrupted") from exc
            repaired = bool(getattr(doc, "is_repaired", False))
        if sum(len(p.text.strip()) for p in pages) / len(pages) < MIN_AVG_CHARS_PER_PAGE:
            raise AppError("corrupted" if repaired else "no_text_layer")
        return pages
