from fastapi import FastAPI

from app.api import ask, documents, documents_upload, health
from app.core.config import get_settings
from app.core.errors import install_error_handlers
from app.core.logging import configure_logging, install_request_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title="Tra cứu quy chế — API",
        version="0.1.0",
        docs_url="/api/v1/docs",
        openapi_url="/api/v1/openapi.json",
    )
    install_error_handlers(app)
    install_request_logging(app)

    app.include_router(health.router)
    app.include_router(documents_upload.router, prefix="/api/v1")
    app.include_router(documents.router, prefix="/api/v1")
    app.include_router(ask.router, prefix="/api/v1")
    return app


app = create_app()
