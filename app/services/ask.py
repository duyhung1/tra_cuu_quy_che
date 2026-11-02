"""Ask service (TASK-009, SAD §3.3): retrieve → resolve → answer, 30 s timeout, usage record."""

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeout
from datetime import date

from app.config import Settings
from app.domain.errors import AppError
from app.domain.text import content_terms
from app.domain.types import Answer, UsageRecord
from app.ports import Answerer, Clock, DocumentStore, Retriever, UsageLog
from app.services.resolver import resolve

log = logging.getLogger("tcqc.ask")
MAX_QUESTION = 2000
_pool = ThreadPoolExecutor(max_workers=16)


class SystemClock:
    def __init__(self, fixed: str | None = None) -> None:
        self._fixed = date.fromisoformat(fixed) if fixed else None

    def today(self) -> date:
        return self._fixed or date.today()


class AskService:
    def __init__(self, store: DocumentStore, retriever: Retriever, answerer: Answerer, usage: UsageLog,
                 clock: Clock, settings: Settings) -> None:
        self.store, self.retriever, self.answerer = store, retriever, answerer
        self.usage, self.clock, self.settings = usage, clock, settings
        self._revision = -1

    def _refresh(self) -> None:
        if self.store.revision != self._revision:
            self.retriever.rebuild(self.store.ready_units())
            self._revision = self.store.revision

    def _pipeline(self, q: str) -> Answer:
        self._refresh()
        units = self.store.ready_units()
        docs = self.store.documents_by_id()
        hits = self.retriever.search(q, self.settings.top_k)
        res = resolve(q, hits, units, self.store.amendments(), docs, self.clock.today(), self.retriever,
                      self.settings.threshold, self.settings.min_coverage)
        siblings = []
        if res.primary is not None and res.primary.clause_no:
            qset = set(content_terms(q))
            siblings = [
                u for u in units
                if u.document_id == res.primary.document_id and u.article_no == res.primary.article_no
                and u.id != res.primary.id and u.clause_no and len(qset & set(content_terms(u.body))) >= 2
                and u not in res.superseded
            ]
        return self.answerer.answer(q, res, docs, siblings)

    def ask(self, question: str) -> tuple[Answer, int]:
        q = (question or "").strip()
        if not 1 <= len(q) <= MAX_QUESTION:
            raise AppError("question_invalid")
        if self.store.count() == 0:
            raise AppError("no_documents")
        start = time.perf_counter()
        status, answer = "ok", None
        try:
            answer = _pool.submit(self._pipeline, q).result(timeout=self.settings.timeout_s)
        except FutureTimeout:
            status = "error"
            log.error("ask_timeout")
        except Exception:
            status = "error"
            log.exception("ask_failed")
        latency = round((time.perf_counter() - start) * 1000)
        try:
            self.usage.record(UsageRecord(latency, status, len(answer.sources) if answer else 0))
        except Exception:  # FR-017: never lose the answer because of the usage log
            log.exception("usage_record_failed")
        if answer is None:
            raise AppError("ai_unavailable")
        log.info("ask_done", extra={"latency_ms": latency, "cited_count": len(answer.sources), "found": answer.found})
        return answer, latency
