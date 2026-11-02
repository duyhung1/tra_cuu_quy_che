"""Ingestion worker process (T-010): `python -m app.worker.main`."""

import asyncio
import signal
import time

import structlog

from app.modules.documents.adapters import job_queue
from app.modules.qa.adapters.tei_embedding import TEIEmbedding
from app.platform.config import get_settings
from app.platform.db import get_engine
from app.platform.logging import configure_logging
from app.platform.storage import S3Storage
from app.worker.ingest import run_ingest

log = structlog.get_logger("worker")
STALE_CHECK_EVERY_S = 60


async def run_forever(stop: asyncio.Event) -> None:
    settings = get_settings()
    engine = get_engine()
    storage = S3Storage(settings)
    embedder = TEIEmbedding(settings.tei_url, timeout_s=30.0)
    last_stale_check = 0.0
    log.info("worker_started")

    while not stop.is_set():
        if time.monotonic() - last_stale_check > STALE_CHECK_EVERY_S:
            async with engine.begin() as conn:
                n = await job_queue.reclaim_stale_jobs(conn, settings.worker_stale_job_minutes)
            if n:
                log.warning("stale_jobs_reclaimed", count=n)
            last_stale_check = time.monotonic()

        async with engine.begin() as conn:
            job = await job_queue.claim_job(conn)
        if job is None:
            try:
                await asyncio.wait_for(stop.wait(), timeout=settings.worker_poll_s)
            except TimeoutError:
                pass
            continue
        # A running job is always finished, even if SIGTERM arrives meanwhile.
        await run_ingest(job, engine=engine, storage=storage, embedder=embedder, settings=settings)

    log.info("worker_stopped")


def main() -> None:
    configure_logging(get_settings().log_level)
    stop = asyncio.Event()

    async def _run() -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, stop.set)
        await run_forever(stop)

    asyncio.run(_run())


if __name__ == "__main__":
    main()
