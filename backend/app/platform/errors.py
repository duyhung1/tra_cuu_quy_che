"""Application errors rendered as RFC 9457 problem+json.

Every code the frontend may receive is listed in ERRORS so the vi.json mapping
on the client stays in sync with the backend.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

ERRORS: dict[str, tuple[int, str]] = {
    "not_pdf": (422, "Not a valid PDF file"),
    "file_too_large": (413, "File exceeds the size limit"),
    "too_many_files": (422, "Too many files in one upload"),
    "duplicate_name": (409, "A document with this name already exists"),
    "collection_full": (409, "Document collection is full"),
    "question_invalid": (422, "Question is empty or too long"),
    "no_documents": (409, "No ready documents to answer from"),
    "ai_unavailable": (503, "AI service unavailable"),
    "storage_error": (502, "Object storage error"),
    "not_found": (404, "Not found"),
    "internal_error": (500, "Internal server error"),
}


class AppError(Exception):
    def __init__(self, code: str, detail: str = "") -> None:
        if code not in ERRORS:
            raise ValueError(f"unknown error code: {code}")
        self.code = code
        self.status, self.title = ERRORS[code]
        self.detail = detail
        super().__init__(f"{code}: {detail}")

    def to_problem(self) -> dict:
        body = {"type": "about:blank", "title": self.title, "status": self.status, "code": self.code}
        if self.detail:
            body["detail"] = self.detail
        return body


def problem_response(code: str, detail: str = "") -> JSONResponse:
    err = AppError(code, detail)
    return JSONResponse(err.to_problem(), status_code=err.status, media_type="application/problem+json")


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(exc.to_problem(), status_code=exc.status, media_type="application/problem+json")

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        # The only JSON body in the API is /ask, so body validation errors map to question_invalid.
        return problem_response("question_invalid", "; ".join(str(e.get("msg", "")) for e in exc.errors()))

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception) -> JSONResponse:
        import structlog

        structlog.get_logger().exception("unhandled_error", path=request.url.path)
        return problem_response("internal_error")
