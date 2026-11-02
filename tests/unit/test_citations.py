from datetime import date

from app.modules.answer.citations import build_sources, cited_refs, strip_invalid_markers
from app.ports.ai import RetrievedChunk

CHUNKS = [
    RetrievedChunk("QC.pdf", 3, "Điều 5 ...", 0.9, article="Điều 5", doc_number="08/2025/QC-SM",
                   effective_date=date(2025, 1, 1)),
    RetrievedChunk("QD.pdf", 1, "Điều 1 ...", 0.8, article="Điều 1", doc_title="QUYẾT ĐỊNH"),
]


def test_cited_refs_are_distinct_ordered_and_in_range():
    assert cited_refs("A [2]. B [1, 2]. C [9]. D [2]", 2) == [2, 1]
    assert cited_refs("Không có căn cứ.", 2) == []


def test_invalid_markers_are_removed():
    assert strip_invalid_markers("Mức 450.000 đồng [2, 7]. Cũ [9].", 2) == "Mức 450.000 đồng [2]. Cũ."
    assert strip_invalid_markers("Không đổi [1].", 2) == "Không đổi [1]."


def test_build_sources_maps_refs_to_chunks():
    sources = build_sources("Áp dụng 450.000 đồng [2], thay mức cũ [1].", CHUNKS)
    assert [(s.ref, s.article, s.filename) for s in sources] == [(2, "Điều 1", "QD.pdf"), (1, "Điều 5", "QC.pdf")]
    assert sources[1].as_dict()["effective_date"] == "2025-01-01"
    assert sources[0].as_dict()["doc_title"] == "QUYẾT ĐỊNH"
