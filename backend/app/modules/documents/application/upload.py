"""Upload use case (T-009).

Validates the whole batch first, then each file independently: one bad file
never prevents the others from being stored.
"""

import os
import tempfile
import unicodedata
import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from typing import IO, Protocol

from sqlalchemy.ext.asyncio import AsyncConnection

from app.modules.documents.adapters import sql_repo
from app.platform.config import Settings
from app.platform.errors import AppError
from app.platform.storage import ObjectStoragePort

PDF_MAGIC = b"%PDF-"
READ_BLOCK = 1024 * 1024


class IncomingFile(Protocol):
    filename: str | None

    async def read(self, size: int = -1) -> bytes: ...


@dataclass
class UploadResult:
    filename: str
    document_id: str | None = None
    status: str | None = None
    error_code: str | None = None

    def as_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


def normalize_filename(raw: str | None) -> str:
    name = os.path.basename((raw or "").replace("\\", "/")).strip()
    name = unicodedata.normalize("NFC", name)
    return (name or "tai_lieu.pdf")[:255]


async def _spool(file: IncomingFile, max_bytes: int) -> tuple[IO[bytes] | None, int, str | None]:
    """Stream the upload to a temp file. Returns (fileobj, size, error_code)."""
    spool = tempfile.SpooledTemporaryFile(max_size=4 * READ_BLOCK)
    size = 0
    first = True
    while block := await file.read(READ_BLOCK):
        if first:
            first = False
            if not block.startswith(PDF_MAGIC):
                spool.close()
                return None, 0, "not_pdf"
        size += len(block)
        if size > max_bytes:
            spool.close()
            return None, 0, "file_too_large"
        spool.write(block)
    if size == 0:
        spool.close()
        return None, 0, "not_pdf"
    spool.seek(0)
    return spool, size, None


async def upload_documents(
    conn: AsyncConnection, storage: ObjectStoragePort, settings: Settings, files: Sequence[IncomingFile]
) -> list[UploadResult]:
    if not files or len(files) > settings.upload_max_files:
        raise AppError("too_many_files")
    if await sql_repo.count_documents(conn) + len(files) > settings.collection_max_docs:
        raise AppError("collection_full")

    names = [normalize_filename(f.filename) for f in files]
    taken = await sql_repo.existing_filenames(conn, names)
    seen_in_batch: set[str] = set()
    results: list[UploadResult] = []

    for file, name in zip(files, names, strict=True):
        if name in taken or name in seen_in_batch:
            results.append(UploadResult(filename=name, error_code="duplicate_name"))
            continue
        fileobj, size, error = await _spool(file, settings.upload_max_bytes)
        if error:
            results.append(UploadResult(filename=name, error_code=error))
            continue
        assert fileobj is not None

        doc_id = uuid.uuid4()
        key = f"documents/{doc_id}.pdf"
        try:
            await storage.put_stream(key, fileobj)
        except AppError:
            results.append(UploadResult(filename=name, error_code="storage_error"))
            continue
        finally:
            fileobj.close()

        # Savepoint per file: a DB failure on one file must not roll back the others.
        try:
            async with conn.begin_nested():
                await sql_repo.insert_document_with_job(
                    conn, doc_id=doc_id, filename=name, size_bytes=size, storage_key=key
                )
        except Exception:
            await storage.delete(key)
            results.append(UploadResult(filename=name, error_code="storage_error"))
            continue

        seen_in_batch.add(name)
        results.append(UploadResult(filename=name, document_id=str(doc_id), status="queued"))
    return results
