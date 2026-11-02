"""Ingestion service (TASK-004, SAD §3.2, ADR-004). Each file is handled independently (FR-002)."""

import logging
import os
import time
import unicodedata

from app.config import Settings
from app.domain.errors import AppError
from app.domain.types import IngestResult
from app.ports import DocumentStore, PdfExtractor
from app.services.legal_parser import parse

log = logging.getLogger("tcqc.ingest")
PDF_MAGIC = b"%PDF-"


def normalize_filename(raw: str | None) -> str:
    name = os.path.basename((raw or "").replace("\\", "/")).strip()
    return (unicodedata.normalize("NFC", name) or "van_ban.pdf")[:255]


class Ingestor:
    def __init__(self, store: DocumentStore, pdf: PdfExtractor, settings: Settings) -> None:
        self.store, self.pdf, self.settings = store, pdf, settings

    def ingest_batch(self, files: list[tuple[str | None, bytes]]) -> list[IngestResult]:
        if not files or len(files) > self.settings.max_files:
            raise AppError("too_many_files")
        results, seen = [], set()
        accepted = self.store.count()
        for raw_name, data in files:
            name = normalize_filename(raw_name)
            code = None
            if accepted >= self.settings.max_documents:
                code = "collection_full"
            elif not data.startswith(PDF_MAGIC):
                code = "not_pdf"
            elif len(data) > self.settings.max_bytes:
                code = "file_too_large"
            elif name in seen or self.store.exists(name):
                code = "duplicate_name"
            if code:
                results.append(self._reject(name, code))
                continue
            seen.add(name)
            result = self._ingest_one(name, data)
            if result.status == "ready":
                accepted += 1
            results.append(result)
        return results

    def _reject(self, name: str, code: str) -> IngestResult:
        err = AppError(code)
        return IngestResult(name, "failed", error_code=code, message=err.message)

    def _ingest_one(self, name: str, data: bytes) -> IngestResult:
        start = time.perf_counter()
        try:
            pages = self.pdf.extract(data, self.settings.max_pages)
            parsed = parse(pages)
            doc_id = self.store.add(name, len(data), len(pages), parsed)
        except AppError as exc:
            self.store.add_failed(name, len(data), exc.code)
            log.info("ingest_failed", extra={"error_code": exc.code})
            return IngestResult(name, "failed", error_code=exc.code, message=exc.message)
        except Exception:
            log.exception("ingest_storage_error")
            return self._reject(name, "storage_error")
        log.info("ingest_done", extra={"document_id": doc_id, "pages": len(pages), "units": len(parsed.units),
                                       "filtered": parsed.filtered,
                                       "processing_ms": round((time.perf_counter() - start) * 1000)})
        return IngestResult(name, "ready", document_id=doc_id)
