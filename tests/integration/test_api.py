"""TASK-005/006/009: API contract, usage log without content, failures (US-001, US-003, US-007, US-009, US-010)."""

from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(settings, pdfs):
    app = create_app(settings)
    c = TestClient(app, raise_server_exceptions=False)
    c.app_state = app.state
    return c


def upload_samples(client, pdfs):
    files = [("files", (p.name, p.read_bytes(), "application/pdf")) for p in sorted((pdfs / "sample").glob("*.pdf"))]
    return client.post("/api/documents", files=files)


def test_healthz(client):
    assert client.get("/healthz").json() == {"status": "ok"}


def test_no_documents_then_upload_then_list(client, pdfs):
    r = client.post("/api/ask", json={"question": "Phụ cấp?"})
    assert r.status_code == 409 and r.json()["code"] == "no_documents"
    assert all(i["status"] == "ready" for i in upload_samples(client, pdfs).json()["items"])
    listing = client.get("/api/documents").json()
    assert listing["counts"] == {"ready": 5, "processing": 0, "failed": 0, "total": 5}
    nq = next(i for i in listing["items"] if i["doc_number"] == "15/2025/NQ-SM")
    assert nq["effective_date"] == "2025-03-10" and nq["title"] == "NỘI QUY LAO ĐỘNG"


def test_eleven_files_is_400(client):
    files = [("files", (f"{i}.pdf", b"%PDF-1.7", "application/pdf")) for i in range(11)]
    r = client.post("/api/documents", files=files)
    assert r.status_code == 400 and r.json() == {"code": "too_many_files", "message": "Mỗi lần chỉ tải tối đa 10 tệp"}


@pytest.mark.parametrize("q", ["", "   ", "x" * 2001])
def test_invalid_question_is_422(client, pdfs, q):
    upload_samples(client, pdfs)
    r = client.post("/api/ask", json={"question": q})
    assert r.status_code == 422 and r.json()["code"] == "question_invalid"


def test_ask_returns_sources_and_one_usage_record_without_text(client, pdfs):
    upload_samples(client, pdfs)
    q = "Mức chi tiếp khách tối đa mỗi lần là bao nhiêu?"
    body = client.post("/api/ask", json={"question": q}).json()
    assert body["found"] and body["sources"][0]["article"] == "Điều 8" and body["latency_ms"] >= 0
    rows = client.app_state.store.usage()
    assert len(rows) == 1 and set(rows[0]) == {"id", "at", "latency_ms", "status", "cited_count"}
    assert rows[0]["status"] == "ok" and rows[0]["cited_count"] == 1


def test_answerer_failure_is_503_and_logged_as_error(client, pdfs, monkeypatch):
    upload_samples(client, pdfs)
    ask = client.app_state.ask

    def boom(*a, **k):
        raise RuntimeError("down")

    monkeypatch.setattr(ask.answerer, "answer", boom)
    r = client.post("/api/ask", json={"question": "Phụ cấp lưu trú bao nhiêu?"})
    assert r.status_code == 503 and r.json()["code"] == "ai_unavailable"
    assert client.app_state.store.usage()[-1]["status"] == "error"


def test_usage_log_failure_still_answers(client, pdfs, monkeypatch):
    upload_samples(client, pdfs)

    def boom(_):
        raise RuntimeError("disk full")

    monkeypatch.setattr(client.app_state.ask.usage, "record", boom)
    r = client.post("/api/ask", json={"question": "Mức chi tiếp khách tối đa mỗi lần là bao nhiêu?"})
    assert r.status_code == 200 and r.json()["found"]


def test_ten_concurrent_questions(client, pdfs):
    upload_samples(client, pdfs)
    with ThreadPoolExecutor(10) as ex:
        codes = list(ex.map(lambda _: client.post("/api/ask", json={"question": "Thời giờ làm việc?"}).status_code,
                            range(10)))
    assert codes == [200] * 10


def test_ui_is_served(client):
    r = client.get("/")
    assert r.status_code == 200 and 'data-testid="ask-input"' in r.text


def test_timeout_is_503_and_logged(settings, pdfs, monkeypatch):
    """CR-R-02 / FR-015: a pipeline slower than timeout_s returns 503 and an error usage record."""
    import time
    from dataclasses import replace

    app = create_app(replace(settings, timeout_s=0.2))
    c = TestClient(app, raise_server_exceptions=False)
    upload_samples(c, pdfs)
    monkeypatch.setattr(app.state.ask, "_pipeline", lambda q: time.sleep(1))
    r = c.post("/api/ask", json={"question": "Thời giờ làm việc?"})
    assert r.status_code == 503 and r.json()["code"] == "ai_unavailable"
    assert app.state.store.usage()[-1]["status"] == "error"


def test_rebuild_during_questions_never_fails(client, pdfs):
    """CR-R-01: uploads (index rebuilds) racing with questions never produce 503."""
    from tests.fixtures.make_pdfs import text_pdf

    upload_samples(client, pdfs)

    def upload(i):
        doc = text_pdf([f"Điều 1. Quy định {i}\n1. Nội dung bổ sung số {i} về chế độ làm việc của nhân viên."])
        return client.post("/api/documents", files=[("files", (f"extra_{i}.pdf", doc, "application/pdf"))]).status_code

    def ask(_):
        return client.post("/api/ask", json={"question": "Thời giờ làm việc từ mấy giờ?"}).status_code

    with ThreadPoolExecutor(12) as ex:
        futures = [ex.submit(upload, i) for i in range(4)] + [ex.submit(ask, i) for i in range(20)]
        codes = [f.result() for f in futures]
    assert set(codes) == {200}


def test_store_releases_the_database_file(settings, pdfs):
    """DEF-001: every connection is closed, so the DB file can be deleted (recovery drill, NFR-005)."""
    import os

    from app import wiring

    store, ing, _ = wiring.build(settings)
    ing.ingest_batch([(p.name, p.read_bytes()) for p in sorted((pdfs / "sample").glob("*.pdf"))])
    assert store.count() == 5
    for suffix in ("", "-wal", "-shm"):
        if os.path.exists(settings.db_path + suffix):
            os.remove(settings.db_path + suffix)
    assert not os.path.exists(settings.db_path)
