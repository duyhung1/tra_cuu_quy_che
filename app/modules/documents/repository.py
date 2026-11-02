"""SQL access for documents (T-009, T-014)."""

import uuid

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from app.models.tables import documents, ingestion_jobs


async def count_documents(conn: AsyncConnection) -> int:
    return (await conn.execute(select(func.count()).select_from(documents))).scalar_one()


async def existing_filenames(conn: AsyncConnection, names: list[str]) -> set[str]:
    if not names:
        return set()
    rows = await conn.execute(select(documents.c.filename).where(documents.c.filename.in_(names)))
    return {r[0] for r in rows}


async def insert_document_with_job(
    conn: AsyncConnection, *, doc_id: uuid.UUID, filename: str, size_bytes: int, storage_key: str
) -> None:
    await conn.execute(
        insert(documents).values(
            id=doc_id, filename=filename, size_bytes=size_bytes, storage_key=storage_key, status="queued"
        )
    )
    await conn.execute(insert(ingestion_jobs).values(document_id=doc_id))


async def list_documents(conn: AsyncConnection) -> list[dict]:
    rows = await conn.execute(
        select(
            documents.c.id,
            documents.c.filename,
            documents.c.pages,
            documents.c.uploaded_at,
            documents.c.status,
            documents.c.error_code,
            documents.c.doc_number,
            documents.c.title,
            documents.c.effective_date,
        ).order_by(documents.c.uploaded_at.desc())
    )
    return [dict(r._mapping) for r in rows]


async def ready_count(conn: AsyncConnection) -> int:
    stmt = select(func.count()).select_from(documents).where(documents.c.status == "ready")
    return (await conn.execute(stmt)).scalar_one()
