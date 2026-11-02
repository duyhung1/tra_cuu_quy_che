"""DocumentStore + UsageLog on SQLite (TASK-005, blueprint §4, ADR-002).
ask_log stores numbers only — never question or answer text (NFR-003)."""

import os
import sqlite3
import threading
from datetime import UTC, date, datetime

from app.domain.types import Amendment, Document, ParsedDocument, Unit, UsageRecord

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY,
  filename TEXT NOT NULL UNIQUE,
  title TEXT, doc_number TEXT, effective_date TEXT, signed_date TEXT,
  pages INTEGER, size_bytes INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('processing','ready','failed')),
  error_code TEXT, units_filtered INTEGER NOT NULL DEFAULT 0,
  uploaded_at TEXT NOT NULL,
  CHECK (status <> 'failed' OR error_code IS NOT NULL)
);
CREATE TABLE IF NOT EXISTS units (
  id INTEGER PRIMARY KEY,
  document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chapter TEXT, article_no TEXT, article_title TEXT, clause_no INTEGER NOT NULL DEFAULT 0,
  page INTEGER NOT NULL, text TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS amendments (
  id INTEGER PRIMARY KEY,
  source_unit_id INTEGER NOT NULL REFERENCES units(id) ON DELETE CASCADE,
  target_doc_number TEXT NOT NULL, target_article_no TEXT NOT NULL, target_clause_no INTEGER
);
CREATE TABLE IF NOT EXISTS ask_log (
  id INTEGER PRIMARY KEY, at TEXT NOT NULL, latency_ms INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('ok','error')), cited_count INTEGER NOT NULL
);
"""


def _d(v: str | None) -> date | None:
    return date.fromisoformat(v) if v else None


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class SqliteStore:
    def __init__(self, path: str) -> None:
        self.path = path
        self.revision = 0
        self._lock = threading.Lock()
        if os.path.dirname(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with self._conn() as c:
            c.execute("PRAGMA journal_mode=WAL")
            c.executescript(SCHEMA)

    def _conn(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.path, timeout=10)
        c.execute("PRAGMA foreign_keys=ON")
        c.row_factory = sqlite3.Row
        return c

    def count(self) -> int:
        with self._conn() as c:
            return c.execute("SELECT count(*) FROM documents WHERE status='ready'").fetchone()[0]

    def exists(self, filename: str) -> bool:
        with self._conn() as c:
            return c.execute("SELECT 1 FROM documents WHERE filename=? AND status='ready'", (filename,)).fetchone() is not None

    def add(self, filename: str, size: int, pages: int, parsed: ParsedDocument) -> int:
        """One transaction per file: document + units + amendments (SAD §3.2 step 6)."""
        with self._lock, self._conn() as c:
            c.execute("DELETE FROM documents WHERE filename=? AND status='failed'", (filename,))
            cur = c.execute(
                "INSERT INTO documents (filename,title,doc_number,effective_date,signed_date,pages,size_bytes,status,"
                "units_filtered,uploaded_at) VALUES (?,?,?,?,?,?,?,'ready',?,?)",
                (filename, parsed.title, parsed.doc_number,
                 parsed.effective_date.isoformat() if parsed.effective_date else None,
                 parsed.signed_date.isoformat() if parsed.signed_date else None,
                 pages, size, parsed.filtered, _now()),
            )
            doc_id = cur.lastrowid
            ids = []
            for u in parsed.units:
                ids.append(c.execute(
                    "INSERT INTO units (document_id,chapter,article_no,article_title,clause_no,page,text) VALUES (?,?,?,?,?,?,?)",
                    (doc_id, u.chapter, u.article_no, u.article_title, u.clause_no, u.page, u.text),
                ).lastrowid)
            for idx, tdoc, tart, tclause in parsed.amendments:
                c.execute(
                    "INSERT INTO amendments (source_unit_id,target_doc_number,target_article_no,target_clause_no) "
                    "VALUES (?,?,?,?)",
                    (ids[idx], tdoc, tart, tclause),
                )
            self.revision += 1
            return doc_id

    def add_failed(self, filename: str, size: int, code: str) -> int:
        with self._lock, self._conn() as c:
            c.execute("DELETE FROM documents WHERE filename=? AND status='failed'", (filename,))
            cur = c.execute(
                "INSERT INTO documents (filename,size_bytes,status,error_code,uploaded_at) VALUES (?,?,'failed',?,?)",
                (filename, size, code, _now()),
            )
            return cur.lastrowid

    def _doc(self, r: sqlite3.Row) -> Document:
        return Document(r["id"], r["filename"], r["title"], r["doc_number"], _d(r["effective_date"]), _d(r["signed_date"]),
                        r["pages"], r["status"], r["error_code"], r["units_filtered"])

    def list_documents(self) -> list[Document]:
        with self._conn() as c:
            return [self._doc(r) for r in c.execute("SELECT * FROM documents ORDER BY id DESC")]

    def documents_by_id(self) -> dict[int, Document]:
        return {d.id: d for d in self.list_documents()}

    def ready_units(self) -> list[Unit]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT u.* FROM units u JOIN documents d ON d.id=u.document_id WHERE d.status='ready' ORDER BY u.id"
            ).fetchall()
        return [Unit(r["id"], r["document_id"], r["chapter"], r["article_no"], r["article_title"], r["clause_no"],
                     r["page"], r["text"]) for r in rows]

    def amendments(self) -> list[Amendment]:
        with self._conn() as c:
            return [Amendment(r["source_unit_id"], r["target_doc_number"], r["target_article_no"], r["target_clause_no"])
                    for r in c.execute("SELECT * FROM amendments")]

    def record(self, rec: UsageRecord) -> None:
        with self._conn() as c:
            c.execute("INSERT INTO ask_log (at,latency_ms,status,cited_count) VALUES (?,?,?,?)",
                      (_now(), rec.latency_ms, rec.status, rec.cited_count))

    def usage(self) -> list[dict]:
        with self._conn() as c:
            return [dict(r) for r in c.execute("SELECT * FROM ask_log ORDER BY id")]
