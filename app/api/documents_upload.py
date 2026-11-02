"""POST /api/v1/documents: multipart upload, one result per file (T-201)."""

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncConnection

from app.api.deps import get_storage
from app.core.config import get_settings
from app.core.db import get_db
from app.modules.documents.upload import upload_documents
from app.ports.storage import ObjectStoragePort

router = APIRouter(tags=["documents"])


@router.post("/documents", status_code=202)
async def upload(
    files: list[UploadFile] = File(default_factory=list),
    conn: AsyncConnection = Depends(get_db),
    storage: ObjectStoragePort = Depends(get_storage),
) -> JSONResponse:
    results = await upload_documents(conn, storage, get_settings(), files)
    return JSONResponse({"items": [r.as_dict() for r in results]}, status_code=202)
