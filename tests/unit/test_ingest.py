"""TASK-004: per-file validation and independence (US-001-AC1..AC6, US-008-AC1)."""

import pytest

from app import wiring
from app.config import Settings
from app.domain.errors import AppError
from tests.fixtures.make_pdfs import many_pages_pdf, text_pdf

GOOD = ["Điều 1. Nội dung\nNội dung hợp lệ đủ dài cho trang văn bản này."]


def codes(results):
    return {r.filename: r.error_code or r.status for r in results}


def test_three_valid_documents_become_ready(settings, pdfs):
    _, ing, _ = wiring.build(settings)
    res = ing.ingest_batch([(p.name, p.read_bytes()) for p in sorted((pdfs / "sample").glob("*.pdf"))[:3]])
    assert [r.status for r in res] == ["ready"] * 3


def test_bad_files_get_one_reason_each_and_do_not_block_valid_ones(settings, pdfs):
    _, ing, _ = wiring.build(settings)
    files = [("ok.pdf", text_pdf(GOOD))] + [(p.name, p.read_bytes()) for p in (pdfs / "bad").glob("*.pdf")]
    assert codes(ing.ingest_batch(files)) == {
        "ok.pdf": "ready", "scan.pdf": "no_text_layer", "mat_khau.pdf": "encrypted_pdf",
        "hong.pdf": "corrupted", "khong_phai_pdf.pdf": "not_pdf",
    }


def test_eleven_files_rejected_as_a_batch(settings):
    _, ing, _ = wiring.build(settings)
    with pytest.raises(AppError) as e:
        ing.ingest_batch([(f"{i}.pdf", b"%PDF-") for i in range(11)])
    assert e.value.code == "too_many_files"


def test_duplicate_too_large_too_many_pages(settings):
    _, ing, _ = wiring.build(settings)
    good = text_pdf(GOOD)
    ing.ingest_batch([("a.pdf", good)])
    res = ing.ingest_batch([("a.pdf", good), ("big.pdf", b"%PDF-" + b"0" * (20 * 1024 * 1024)),
                            ("long.pdf", many_pages_pdf(301))])
    assert codes(res) == {"a.pdf": "duplicate_name", "big.pdf": "file_too_large", "long.pdf": "too_many_pages"}


def test_collection_full(tmp_path):
    _, ing, _ = wiring.build(Settings(db_path=str(tmp_path / "f.db"), max_documents=2))
    good = text_pdf(GOOD)
    assert codes(ing.ingest_batch([("1.pdf", good), ("2.pdf", good), ("3.pdf", good)]))["3.pdf"] == "collection_full"


def test_injected_instruction_is_dropped(built):
    store, _, _ = built
    tb = next(d for d in store.list_documents() if d.doc_number == "09/2026/TB-SM")
    assert tb.units_filtered == 1
    assert all("1 tỷ" not in u.text for u in store.ready_units())
