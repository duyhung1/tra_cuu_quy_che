"""Ingestion job queue on PostgreSQL (T-010).

Workers claim jobs with FOR UPDATE SKIP LOCKED, so several workers can run in
parallel without picking the same job.
"""

import uuid
from datetime import timedelta

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.domain import Job

CLAIM_SQL = text(
    """
    UPDATE ingestion_jobs j
       SET state = 'running', started_at = now(), attempt = j.attempt + 1
     WHERE j.id = (SELECT id FROM ingestion_jobs
                    WHERE state IN ('queued','retrying') AND next_run_at <= now()
                    ORDER BY next_run_at
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1)
    RETURNING j.id, j.document_id, j.attempt
    """
)

RECLAIM_STALE_SQL = text(
    """
    UPDATE ingestion_jobs SET state = 'retrying', next_run_at = now()
     WHERE state = 'running' AND started_at < now() - make_interval(mins => :minutes)
    """
)


async def claim_job(conn: AsyncConnection) -> Job | None:
    row = (await conn.execute(CLAIM_SQL)).first()
    if row is None:
        return None
    await conn.execute(
        text("UPDATE documents SET status = 'processing' WHERE id = :id AND status <> 'ready'"),
        {"id": row.document_id},
    )
    return Job(id=row.id, document_id=row.document_id, attempt=row.attempt)


async def reclaim_stale_jobs(conn: AsyncConnection, minutes: int) -> int:
    return (await conn.execute(RECLAIM_STALE_SQL, {"minutes": minutes})).rowcount


async def mark_succeeded(conn: AsyncConnection, job_id: uuid.UUID, processing_ms: int) -> None:
    await conn.execute(
        text(
            "UPDATE ingestion_jobs SET state='succeeded', finished_at=now(), processing_ms=:ms, error=NULL "
            "WHERE id=:id"
        ),
        {"id": job_id, "ms": processing_ms},
    )


async def mark_failed(conn: AsyncConnection, job: Job, error_code: str, error: str) -> None:
    await conn.execute(
        text("UPDATE ingestion_jobs SET state='failed', finished_at=now(), error=:err WHERE id=:id"),
        {"id": job.id, "err": error[:2000]},
    )
    await conn.execute(
        text("UPDATE documents SET status='failed', error_code=:code WHERE id=:id"),
        {"id": job.document_id, "code": error_code},
    )


def retry_delay(attempt: int) -> timedelta:
    """10 s, 40 s, 160 s, …"""
    return timedelta(seconds=10 * 4 ** (attempt - 1))


async def mark_retrying(conn: AsyncConnection, job: Job, error: str) -> None:
    await conn.execute(
        text(
            "UPDATE ingestion_jobs SET state='retrying', error=:err, next_run_at=now() + :delay "
            "WHERE id=:id"
        ),
        {"id": job.id, "err": error[:2000], "delay": retry_delay(job.attempt)},
    )
    await conn.execute(
        text("UPDATE documents SET status='queued' WHERE id=:id"), {"id": job.document_id}
    )
