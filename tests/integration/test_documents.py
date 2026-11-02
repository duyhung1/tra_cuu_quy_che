"""T-016: upload API + ingestion pipeline on a real database."""

import asyncio
import io

import httpx
import pytest
from sqlalchemy import select, text

from app.api import deps
from app.core.config import get_settings
from app.main import create_app
from app.models.tables import chunks, documents, ingestion_jobs
from app.modules.jobs import repository as job_queue
from app.worker.ingest import run_ingest
from tests.fakes.fakes import FakeEmbedder, FakeStorage
from tests.fixtures.make_pdfs import (
    SAMPLE_DOCS,
    corrupted_pdf,
    encrypted_pdf,
    fake_pdf,
    many_pages_pdf,
    scanned_pdf,
    text_pdf,
)

pytestmark = pytest.mark.integration


def word_chunker(pages, filename):
    from app.worker.chunker import chunk_document

    return chunk_document(pages, filename, count=lambda t: len(t.split()))


@pytest.fixture
def storage():
    return FakeStorage()


@pytest.fixture
async def client(engine, storage):
    app = create_app()
    app.dependency_overrides[deps.get_storage] = lambda: storage
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as c:
        yield c


def files_payload(items):
    return [("files", (name, io.BytesIO(data), "application/pdf")) for name, data in items]


async def process_all_jobs(engine, storage, embedder=None):
    embedder = embedder or FakeEmbedder()
    while True:
        async with engine.begin() as conn:
            job = await job_queue.claim_job(conn)
        if job is None:
            return
        await run_ingest(job, engine=engine, storage=storage, embedder=embedder,
                         settings=get_settings(), chunker=word_chunker)


async def test_upload_three_valid_pdfs_then_ingest(client, engine, storage):
    payload = files_payload((n, text_pdf(p)) for n, p in SAMPLE_DOCS.items())
    resp = await client.post("/api/v1/documents", files=payload)
    assert resp.status_code == 202
    items = resp.json()["items"]
    assert [i["status"] for i in items] == ["queued"] * 3
    assert len(storage.objects) == 3

    listing = (await client.get("/api/v1/documents")).json()
    assert listing["counts"] == {"ready": 0, "processing": 3, "failed": 0, "total": 3}

    await process_all_jobs(engine, storage)
    listing = (await client.get("/api/v1/documents")).json()
    assert listing["counts"]["ready"] == 3
    assert all(i["pages"] >= 1 for i in listing["items"])
    meta = {i["filename"]: (i["doc_number"], i["effective_date"]) for i in listing["items"]}
    assert meta == {
        "Quy_che_chi_tieu_noi_bo_2025.pdf": ("08/2025/QC-SM", "2025-01-01"),
        "Noi_quy_lao_dong_2025.pdf": ("15/2025/NQ-SM", "2025-03-10"),
        "Quyet_dinh_sua_doi_cong_tac_phi_2026.pdf": ("02/2026/QĐ-SM", "2026-07-01"),
    }
    async with engine.connect() as conn:
        articles = set((await conn.execute(select(chunks.c.article))).scalars())
    assert {"Điều 4", "Điều 5", "Điều 6", "Điều 7"} <= articles


async def test_too_many_files_rejects_whole_batch(client, storage):
    payload = files_payload((f"t{i}.pdf", text_pdf(["x"])) for i in range(11))
    resp = await client.post("/api/v1/documents", files=payload)
    assert resp.status_code == 422 and resp.json()["code"] == "too_many_files"
    assert storage.objects == {}


async def test_per_file_errors_do_not_block_valid_files(client, monkeypatch):
    monkeypatch.setenv("UPLOAD_MAX_MB", "1")
    get_settings.cache_clear()
    big = b"%PDF-1.7\n" + b"0" * (1024 * 1024 + 10)
    payload = files_payload([
        ("ok.pdf", text_pdf(["Nội dung hợp lệ đủ dài cho trang tài liệu này."])),
        ("fake.pdf", fake_pdf()),
        ("big.pdf", big),
    ])
    resp = await client.post("/api/v1/documents", files=payload)
    got = {i["filename"]: i.get("error_code") or i["status"] for i in resp.json()["items"]}
    assert got == {"ok.pdf": "queued", "fake.pdf": "not_pdf", "big.pdf": "file_too_large"}
    get_settings.cache_clear()


async def test_duplicate_name(client):
    data = text_pdf(["Nội dung hợp lệ đủ dài cho trang tài liệu này."])
    await client.post("/api/v1/documents", files=files_payload([("a.pdf", data)]))
    resp = await client.post("/api/v1/documents", files=files_payload([("a.pdf", data)]))
    assert resp.json()["items"][0]["error_code"] == "duplicate_name"


async def test_collection_full(client, monkeypatch):
    monkeypatch.setenv("COLLECTION_MAX_DOCS", "2")
    get_settings.cache_clear()
    data = text_pdf(["Nội dung hợp lệ đủ dài cho trang tài liệu này."])
    await client.post("/api/v1/documents", files=files_payload([("a.pdf", data)]))
    resp = await client.post("/api/v1/documents", files=files_payload([("b.pdf", data), ("c.pdf", data)]))
    assert resp.status_code == 409 and resp.json()["code"] == "collection_full"
    get_settings.cache_clear()


@pytest.mark.parametrize(
    ("name", "data", "code"),
    [
        ("enc.pdf", encrypted_pdf(), "encrypted_pdf"),
        ("scan.pdf", scanned_pdf(), "no_text_layer"),
        ("broken.pdf", corrupted_pdf(), "corrupted"),
        ("long.pdf", many_pages_pdf(301), "too_many_pages"),
    ],
    ids=["encrypted", "scanned", "truncated", "too_many_pages"],
)
async def test_bad_pdfs_fail_with_code(client, engine, storage, name, data, code):
    await client.post("/api/v1/documents", files=files_payload([(name, data)]))
    await process_all_jobs(engine, storage)
    item = (await client.get("/api/v1/documents")).json()["items"][0]
    assert (item["status"], item["error_code"]) == ("failed", code)


async def test_transient_errors_retry_then_give_up(client, engine, storage):
    await client.post("/api/v1/documents",
                      files=files_payload([("a.pdf", text_pdf(["Nội dung đủ dài để có lớp văn bản."]))]))
    for attempt in range(1, 4):
        async with engine.begin() as conn:
            await conn.execute(text("UPDATE ingestion_jobs SET next_run_at = now()"))
            job = await job_queue.claim_job(conn)
        assert job.attempt == attempt
        await run_ingest(job, engine=engine, storage=storage, embedder=FakeEmbedder(fail=True),
                         settings=get_settings(), chunker=word_chunker)
    async with engine.connect() as conn:
        status, code = (await conn.execute(select(documents.c.status, documents.c.error_code))).one()
        state = (await conn.execute(select(ingestion_jobs.c.state))).scalar_one()
    assert (status, code, state) == ("failed", "transient_exhausted", "failed")


async def test_two_workers_never_claim_the_same_job(client, engine):
    data = text_pdf(["Nội dung hợp lệ đủ dài cho trang tài liệu này."])
    await client.post("/api/v1/documents", files=files_payload([(f"d{i}.pdf", data) for i in range(10)]))

    async def worker():
        claimed = []
        while True:
            async with engine.begin() as conn:
                job = await job_queue.claim_job(conn)
            if job is None:
                return claimed
            claimed.append(job.id)

    a, b = await asyncio.gather(worker(), worker())
    assert len(a) + len(b) == 10 and not set(a) & set(b)


async def test_stale_running_job_is_reclaimed(client, engine):
    await client.post("/api/v1/documents",
                      files=files_payload([("a.pdf", text_pdf(["Nội dung đủ dài để có lớp văn bản."]))]))
    async with engine.begin() as conn:
        await job_queue.claim_job(conn)
        await conn.execute(text("UPDATE ingestion_jobs SET started_at = now() - interval '11 minutes'"))
        assert await job_queue.reclaim_stale_jobs(conn, 10) == 1
        assert await job_queue.claim_job(conn) is not None
