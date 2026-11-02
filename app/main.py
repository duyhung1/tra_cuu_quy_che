"""HTTP API (CMP-02, blueprint §5) and static UI (CMP-01)."""

import os
from pathlib import Path

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import logging_setup, wiring
from app.config import Settings, get_settings
from app.domain.errors import AppError

WEB = Path(__file__).resolve().parent.parent / "web"


class AskBody(BaseModel):
    question: str = ""


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    logging_setup.configure(os.environ.get("TCQC_LOG"))
    store, ingestor, ask_service = wiring.build(settings)
    app = FastAPI(title="Tra cứu quy chế", docs_url="/api/docs")
    app.state.store, app.state.ask = store, ask_service

    @app.exception_handler(AppError)
    async def app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse({"code": exc.code, "message": exc.message}, status_code=exc.status)

    @app.get("/healthz")
    def healthz() -> dict:
        return {"status": "ok"}

    @app.post("/api/documents")
    async def upload(files: list[UploadFile] = File(default_factory=list)) -> dict:
        if not files or len(files) > settings.max_files:
            raise AppError("too_many_files")
        payload = []
        for f in files:
            payload.append((f.filename, await f.read(settings.max_bytes + 1)))
        return {"items": [r.as_dict() for r in ingestor.ingest_batch(payload)]}

    @app.get("/api/documents")
    def list_documents() -> dict:
        docs = store.list_documents()
        counts = {"ready": 0, "processing": 0, "failed": 0, "total": len(docs)}
        for d in docs:
            counts[d.status] += 1
        return {
            "items": [
                {"id": d.id, "filename": d.filename, "title": d.title, "doc_number": d.doc_number,
                 "effective_date": d.effective_date.isoformat() if d.effective_date else None, "pages": d.pages,
                 "status": d.status, "error_code": d.error_code,
                 "message": AppError(d.error_code).message if d.error_code else None}
                for d in docs
            ],
            "counts": counts,
            "limit": settings.max_documents,
        }

    @app.post("/api/ask")
    def ask(body: AskBody) -> dict:
        answer, latency = ask_service.ask(body.question)
        return {"answer": answer.text, "found": answer.found, "latency_ms": latency,
                "sources": [s.as_dict() for s in answer.sources]}

    app.mount("/", StaticFiles(directory=WEB, html=True), name="web")
    return app


app = create_app()
