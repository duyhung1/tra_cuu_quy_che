"""GET /api/v1/documents: list with status counts and detected metadata (T-202)."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.config import get_settings
from app.core.db import get_db
from app.modules.documents import repository as doc_repo

router = APIRouter(tags=["documents"])


@router.get("/documents")
async def list_documents(conn: AsyncConnection = Depends(get_db)) -> dict:
    items = await doc_repo.list_documents(conn)
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
