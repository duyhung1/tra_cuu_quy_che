"""Ingestion pipeline for one job (T-013): S3 → extract → metadata → chunk by article → embed → store."""

import time
from collections.abc import Callable

import structlog
from sqlalchemy import delete, insert, select, text
from sqlalchemy.ext.asyncio import AsyncEngine

from app.modules.documents.adapters import job_queue
from app.modules.documents.adapters.job_queue import Job
from app.modules.documents.ingestion.chunker import Chunk, chunk_document
from app.modules.documents.ingestion.legal_structure import detect_metadata
from app.modules.documents.ingestion.pdf_extractor import ExtractedPage, ExtractionError, extract
from app.modules.qa.ports import EmbeddingPort, EmbeddingUnavailable
from app.platform.config import Settings
from app.platform.db_schema import chunks, documents
from app.platform.errors import AppError
from app.platform.storage import ObjectStoragePort

log = structlog.get_logger("ingest")

Chunker = Callable[[list[ExtractedPage], str], list[Chunk]]


async def run_ingest(
    job: Job,
    *,
    engine: AsyncEngine,
    storage: ObjectStoragePort,
    embedder: EmbeddingPort,
    settings: Settings,
    chunker: Chunker = chunk_document,
) -> None:
    start = time.perf_counter()
    async with engine.connect() as conn:
        doc = (
            await conn.execute(
                select(documents.c.filename, documents.c.storage_key).where(documents.c.id == job.document_id)
            )
        ).first()
    if doc is None:  # document deleted while queued
        async with engine.begin() as conn:
            await conn.execute(
                text("UPDATE ingestion_jobs SET state='failed', finished_at=now(), error='document_missing' "
                     "WHERE id=:id"),
                {"id": job.id},
            )
        return

    bound = log.bind(document_id=str(job.document_id), attempt=job.attempt)
    try:
        pdf_bytes = await storage.get_bytes(doc.storage_key)
        pages = extract(pdf_bytes, settings.pdf_max_pages)
        meta = detect_metadata(pages)
        doc_chunks = chunker(pages, doc.filename)
        if not doc_chunks:
            raise ExtractionError("no_text_layer")
        vectors = await embedder.embed([c.embed_text for c in doc_chunks])
    except ExtractionError as exc:
        bound.info("ingest_rejected", error_code=exc.code)
        async with engine.begin() as conn:
            await job_queue.mark_failed(conn, job, exc.code, exc.code)
        return
    except (AppError, EmbeddingUnavailable, OSError) as exc:
        await _transient_failure(engine, job, settings, repr(exc), bound)
        return

    processing_ms = round((time.perf_counter() - start) * 1000)
    try:
        async with engine.begin() as conn:
            await conn.execute(delete(chunks).where(chunks.c.document_id == job.document_id))
            await conn.execute(
                insert(chunks),
                [
                    {
                        "document_id": job.document_id,
                        "chunk_index": c.index,
                        "page_start": c.page_start,
                        "page_end": c.page_end,
                        "content": c.content,
                        "token_count": c.token_count,
                        "article": c.article,
                        "chapter": c.chapter,
                        "embedding": v,
                    }
                    for c, v in zip(doc_chunks, vectors, strict=True)
                ],
            )
            await conn.execute(
                text(
                    "UPDATE documents SET status='ready', pages=:pages, ready_at=now(), error_code=NULL, "
                    "doc_number=:doc_number, title=:title, effective_date=:effective_date "
                    "WHERE id=:id"
                ),
                {
                    "id": job.document_id,
                    "pages": len(pages),
                    "doc_number": meta.doc_number,
                    "title": meta.title,
                    "effective_date": meta.effective_date,
                },
            )
            await job_queue.mark_succeeded(conn, job.id, processing_ms)
    except Exception as exc:  # DB errors are transient from the job's point of view
        await _transient_failure(engine, job, settings, repr(exc), bound)
        return
    bound.info(
        "ingest_done",
        pages=len(pages),
        chunks=len(doc_chunks),
        articles=len({c.article for c in doc_chunks if c.article}),
        processing_ms=processing_ms,
    )


async def _transient_failure(engine: AsyncEngine, job: Job, settings: Settings, error: str, bound) -> None:
    async with engine.begin() as conn:
        if job.attempt < settings.ingest_max_attempts:
            bound.warning("ingest_retry", error=error)
            await job_queue.mark_retrying(conn, job, error)
        else:
            bound.error("ingest_gave_up", error=error)
            await job_queue.mark_failed(conn, job, "transient_exhausted", error)
