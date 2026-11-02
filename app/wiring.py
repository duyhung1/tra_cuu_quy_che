"""Build adapters for each port. Only this file imports app.adapters (SAD §2.3)."""

from app.adapters.bm25 import Bm25Retriever
from app.adapters.pdf_pymupdf import PyMuPdfExtractor
from app.adapters.rule_answerer import RuleBasedAnswerer
from app.adapters.sqlite_store import SqliteStore
from app.config import Settings
from app.services.ask import AskService, SystemClock
from app.services.ingest import Ingestor


def build(settings: Settings) -> tuple[SqliteStore, Ingestor, AskService]:
    store = SqliteStore(settings.db_path)
    ingestor = Ingestor(store, PyMuPdfExtractor(), settings)
    ask = AskService(store, Bm25Retriever(), RuleBasedAnswerer(), store, SystemClock(settings.today), settings)
    return store, ingestor, ask
