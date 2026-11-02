from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.modules.documents.adapters.job_queue import retry_delay
from app.modules.documents.application.upload import normalize_filename
from app.platform.errors import AppError, install_error_handlers


def test_app_error_is_problem_json():
    app = FastAPI()
    install_error_handlers(app)

    @app.get("/boom")
    async def boom():
        raise AppError("not_pdf")

    resp = TestClient(app).get("/boom")
    assert resp.status_code == 422
    assert resp.headers["content-type"].startswith("application/problem+json")
    assert resp.json()["code"] == "not_pdf"


def test_normalize_filename_strips_paths_and_limits_length():
    assert normalize_filename("C:\\Users\\a\\Hợp đồng.pdf") == "Hợp đồng.pdf"
    assert normalize_filename("../../etc/passwd.pdf") == "passwd.pdf"
    assert normalize_filename(None) == "tai_lieu.pdf"
    assert len(normalize_filename("a" * 400 + ".pdf")) == 255


def test_retry_backoff():
    assert [retry_delay(a).total_seconds() for a in (1, 2, 3)] == [10, 40, 160]
