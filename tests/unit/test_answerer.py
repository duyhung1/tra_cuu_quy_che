"""TASK-008: answer text with [n], sources, not-found (US-003-AC2, US-004-AC2, US-005-AC1, US-006-AC1, US-008-AC1)."""

from app.adapters.rule_answerer import NOT_FOUND


def test_positive_answer_has_reference_and_full_source(built):
    _, _, ask = built
    a, _ = ask.ask("Mức chi tiếp khách tối đa mỗi lần là bao nhiêu?")
    assert a.found and "2.000.000" in a.text and "[1]" in a.text
    s = a.sources[0]
    assert (s.article, s.doc_number, s.page) == ("Điều 8", "08/2025/QC-SM", 2)
    assert s.doc_title == "QUY CHẾ CHI TIÊU NỘI BỘ" and s.effective_date.isoformat() == "2025-01-01"


def test_conflict_names_replaced_document_and_old_value(built):
    _, _, ask = built
    a, _ = ask.ask("Phụ cấp lưu trú khi đi công tác hiện nay là bao nhiêu một ngày?")
    assert a.sources[0].doc_number == "02/2026/QĐ-SM"
    assert all(x in a.text for x in ("450.000", "thay thế", "08/2025/QC-SM", "300.000"))


def test_future_rule_is_announced_not_applied(built):
    _, _, ask = built
    a, _ = ask.ask("Người lao động làm việc đủ 12 tháng được nghỉ bao nhiêu ngày phép năm?")
    assert "12 ngày" in a.text.split("\n")[0]
    assert "sắp có hiệu lực từ 01/01/2027" in a.text and "14 ngày" in a.text


def test_not_found_has_fixed_sentence_and_no_sources(built):
    _, _, ask = built
    a, _ = ask.ask("Công ty thưởng Tết bao nhiêu tháng lương?")
    assert a.text == NOT_FOUND and a.sources == [] and not a.found


def test_injected_instruction_never_answers(built):
    _, _, ask = built
    a, _ = ask.ask("Phụ cấp lưu trú là bao nhiêu?")
    assert "1 tỷ" not in a.text
