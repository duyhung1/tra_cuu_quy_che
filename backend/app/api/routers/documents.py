from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncConnection

from app.api.deps import get_storage
from app.modules.documents.adapters import sql_repo
from app.modules.documents.application.upload import upload_documents
from app.platform.config import get_settings
from app.platform.db import get_db
from app.platform.storage import ObjectStoragePort

router = APIRouter(tags=["documents"])


@router.post("/documents", status_code=202)
async def upload(
    files: list[UploadFile] = File(default_factory=list),
    conn: AsyncConnection = Depends(get_db),
    storage: ObjectStoragePort = Depends(get_storage),
) -> JSONResponse:
    results = await upload_documents(conn, storage, get_settings(), files)
    return JSONResponse({"items": [r.as_dict() for r in results]}, status_code=202)


@router.get("/documents")
async def list_documents(conn: AsyncConnection = Depends(get_db)) -> dict:
    items = await sql_repo.list_documents(conn)
    counts = {"ready": 0, "processing": 0, "failed": 0, "total": len(items)}
    for item in items:
        if item["status"] == "ready":
            counts["ready"] += 1
        elif item["status"] in ("queued", "processing"):
            counts["processing"] += 1
        elif item["status"] == "failed":
            counts["failed"] += 1
    return {
        "items": [
            {
                "id": str(i["id"]),
                "filename": i["filename"],
                "pages": i["pages"],
                "uploaded_at": i["uploaded_at"].isoformat(),
                "status": i["status"],
                "error_code": i["error_code"],
                "doc_number": i["doc_number"],
                "title": i["title"],
                "effective_date": i["effective_date"].isoformat() if i["effective_date"] else None,
            }
            for i in items
        ],
        "counts": counts,
        "limit": get_settings().collection_max_docs,
    }
