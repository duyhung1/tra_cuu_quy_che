"""T-022: retrieval + ask endpoint on a real database, with fake embedder / LLM."""

import uuid
from datetime import date

import httpx
import pytest
from sqlalchemy import insert, select

from app.api import deps
from app.main import create_app
from app.models.tables import chunks, documents, qa_log
from app.modules.retrieval.queries import PgRetrieval
from tests.fakes.fakes import FakeEmbedder, FakeLLM, bag_of_words_vector

pytestmark = pytest.mark.integration


async def add_doc(engine, filename, status, texts, **meta):
    doc_id = uuid.uuid4()
    async with engine.begin() as conn:
        await conn.execute(insert(documents).values(
            id=doc_id, filename=filename, size_bytes=100, storage_key=f"documents/{doc_id}.pdf",
            status=status, pages=len(texts), **meta))
        for i, t in enumerate(texts):
            await conn.execute(insert(chunks).values(
                document_id=doc_id, chunk_index=i, page_start=i + 1, page_end=i + 1, article=f"Điều {i + 1}",
                content=t, token_count=len(t.split()), embedding=bag_of_words_vector(t)))
    return doc_id


@pytest.fixture
def llm():
    return FakeLLM("Phụ cấp lưu trú 450.000 đồng/ngày [1].")


@pytest.fixture
async def client(engine, llm):
    app = create_app()
    app.dependency_overrides[deps.get_embedder] = lambda: FakeEmbedder()
    app.dependency_overrides[deps.get_llm] = lambda: llm
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as c:
        yield c


async def test_retrieval_ranks_relevant_chunk_and_skips_unready(engine):
    await add_doc(engine, "A.pdf", "ready", ["giờ làm việc buổi sáng", "phụ cấp lưu trú công tác"],
                  doc_number="08/2025/QC-SM", title="QUY CHẾ", effective_date=date(2025, 1, 1))
    await add_doc(engine, "B.pdf", "processing", ["phụ cấp lưu trú công tác"])
    async with engine.begin() as conn:
        hits = await PgRetrieval(conn).search(bag_of_words_vector("phụ cấp lưu trú"), 5)
    assert hits[0].filename == "A.pdf" and hits[0].page_start == 2 and hits[0].article == "Điều 2"
    assert (hits[0].doc_number, hits[0].doc_title, hits[0].effective_date) == (
        "08/2025/QC-SM", "QUY CHẾ", date(2025, 1, 1))
    assert all(h.filename != "B.pdf" for h in hits)


async def test_ask_returns_answer_with_sources_and_logs_without_content(client, engine, llm):
    await add_doc(engine, "A.pdf", "ready", ["phụ cấp lưu trú 450.000 đồng"], doc_number="02/2026/QĐ-SM")
    resp = await client.post("/api/v1/ask", json={"question": "Phụ cấp lưu trú bao nhiêu?"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["answer"] == "Phụ cấp lưu trú 450.000 đồng/ngày [1]."
    assert body["sources"] == [{
        "ref": 1, "filename": "A.pdf", "page": 1, "article": "Điều 1", "chapter": None,
        "doc_title": None, "doc_number": "02/2026/QĐ-SM", "effective_date": None,
    }]
    assert llm.last_chunks[0].filename == "A.pdf"
    async with engine.connect() as conn:
        row = (await conn.execute(select(qa_log))).one()._mapping
    assert row["status"] == "ok" and row["chunk_count"] == 1 and row["cited_count"] == 1
    assert set(row.keys()) == {"id", "created_at", "status", "latency_ms", "input_tokens", "output_tokens",
                               "chunk_count", "cited_count"}


@pytest.mark.parametrize("body", [{"question": ""}, {"question": "x" * 2001}, {}])
async def test_invalid_question(client, engine, body):
    await add_doc(engine, "A.pdf", "ready", ["nội dung"])
    resp = await client.post("/api/v1/ask", json=body)
    assert resp.status_code == 422 and resp.json()["code"] == "question_invalid"


async def test_no_ready_documents(client, engine):
    await add_doc(engine, "B.pdf", "processing", ["nội dung"])
    resp = await client.post("/api/v1/ask", json={"question": "Có gì?"})
    assert resp.status_code == 409 and resp.json()["code"] == "no_documents"


async def test_llm_failure_is_503_and_logged(client, engine, llm):
    llm.fail = True
    await add_doc(engine, "A.pdf", "ready", ["nội dung"])
    resp = await client.post("/api/v1/ask", json={"question": "Có gì?"})
    assert resp.status_code == 503 and resp.json()["code"] == "ai_unavailable"
    async with engine.connect() as conn:
        assert (await conn.execute(select(qa_log.c.status))).scalar_one() == "error"
