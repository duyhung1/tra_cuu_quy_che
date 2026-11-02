from datetime import date

from app.modules.documents.ingestion.legal_structure import clause_units, detect_metadata, split_sections
from app.modules.documents.ingestion.pdf_extractor import ExtractedPage

DOC = [
    ExtractedPage(
        1,
        "CÔNG TY CỔ PHẦN SAO MAI\nSố: 08/2025/QC-SM\nHà Nội, ngày 20 tháng 12 năm 2024\n\nQUY CHẾ\nCHI TIÊU NỘI BỘ\n\n"
        "Chương I\nQUY ĐỊNH CHUNG\n\nĐiều 1. Phạm vi điều chỉnh\nQuy chế này quy định các khoản chi.\n\n"
        "Chương II. CHẾ ĐỘ CÔNG TÁC PHÍ\nĐiều 5. Phụ cấp lưu trú\n1. Mức 300.000 đồng/ngày.",
    ),
    ExtractedPage(2, "2. Đi trong ngày 150.000 đồng, theo Điều 6 của Quy chế.\nĐiều 6: Phương tiện\nMáy bay."),
]


def test_sections_follow_chapters_and_articles_across_pages():
    sections = split_sections(DOC)
    assert [s.article for s in sections] == [None, "Điều 1", "Điều 5", "Điều 6"]
    preamble, art1, art5, art6 = sections
    assert preamble.text.startswith("CÔNG TY CỔ PHẦN SAO MAI")
    assert art1.chapter == "Chương I. QUY ĐỊNH CHUNG"
    assert art5.chapter == "Chương II. CHẾ ĐỘ CÔNG TÁC PHÍ"
    assert art5.heading == "Điều 5. Phụ cấp lưu trú"
    # Article 5 continues on page 2; "theo Điều 6 của" is a reference, not a heading
    assert (art5.page_start, art5.page_end) == (1, 2)
    assert "Chương" not in art5.text
    assert art6.title == "Phương tiện" and art6.page_start == 2


def test_clause_units_keep_heading_with_first_clause():
    art5 = split_sections(DOC)[2]
    units = clause_units(art5)
    assert [[ln.text[:8] for ln in u] for u in units] == [["Điều 5. ", "1. Mức 3"], ["2. Đi tr"]]


def test_metadata_number_title_and_explicit_effective_date():
    pages = [*DOC, ExtractedPage(3, "Điều 9. Hiệu lực\nQuy chế này có hiệu lực từ ngày 01/01/2025.")]
    meta = detect_metadata(pages)
    assert meta.doc_number == "08/2025/QC-SM"
    assert meta.title == "QUY CHẾ CHI TIÊU NỘI BỘ"
    assert meta.effective_date == date(2025, 1, 1)


def test_effective_on_signing_uses_the_signing_date():
    pages = [
        ExtractedPage(1, "Số: 02/2026/QĐ-SM\nHà Nội, ngày 15 tháng 6 năm 2026\nQUYẾT ĐỊNH\nVề việc sửa đổi phụ cấp"),
        ExtractedPage(2, "Điều 2. Quyết định này có hiệu lực kể từ ngày ký."),
    ]
    meta = detect_metadata(pages)
    assert meta.title == "QUYẾT ĐỊNH Về việc sửa đổi phụ cấp"
    assert meta.effective_date == date(2026, 6, 15)


def test_metadata_is_empty_for_unstructured_text():
    meta = detect_metadata([ExtractedPage(1, "Biên bản họp nhóm, không có số hiệu.")])
    assert (meta.doc_number, meta.title, meta.effective_date) == (None, None, None)
    assert detect_metadata([]).title is None


def test_doc_number_with_soft_hyphen_from_pdf_font():
    meta = detect_metadata([ExtractedPage(1, "Số: 15/2025/NQ\u00adSM\nNỘI QUY LAO ĐỘNG")])
    assert meta.doc_number == "15/2025/NQ-SM"
