"""JSON logs with a fixed set of numeric/ID fields. No question, answer or document text (NFR-003)."""

import json
import logging

ALLOWED = ("document_id", "pages", "units", "filtered", "error_code", "latency_ms", "cited_count", "found",
           "processing_ms", "status", "path", "method")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        out = {"level": record.levelname, "event": record.getMessage()}
        out.update({k: getattr(record, k) for k in ALLOWED if hasattr(record, k)})
        if record.exc_info:
            out["exc_type"] = record.exc_info[0].__name__ if record.exc_info[0] else None
        return json.dumps(out, ensure_ascii=False)


def configure(path: str | None = None) -> None:
    root = logging.getLogger("tcqc")
    root.setLevel(logging.INFO)
    root.handlers.clear()
    handler = logging.FileHandler(path, encoding="utf-8") if path else logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root.addHandler(handler)
