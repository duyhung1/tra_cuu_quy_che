"""TASK-007: effective-date rules — required tests (a)–(f) of blueprint §6.5."""

from datetime import date

from app.adapters.bm25 import Bm25Retriever
from app.domain.types import Amendment, Document, Unit
from app.services.resolver import resolve

T = date(2026, 11, 2)


def doc(i, num, eff):
    return Document(i, f"{i}.pdf", f"DOC {i}", num, eff, None, 1, "ready")


def unit(i, d, art, cl, text):
    return Unit(i, d, None, art, f"Tiêu đề {art}", cl, 1, f"Điều {art}. Tiêu đề {art}\n{text}")


DOCS = {1: doc(1, "08/2025/QC", date(2025, 1, 1)), 2: doc(2, "02/2026/QD", date(2026, 7, 1)),
        3: doc(3, "05/2026/QD", date(2027, 1, 1)), 4: doc(4, "09/2026/QD", date(2026, 9, 1)),
        5: doc(5, None, None)}
U1 = unit(1, 1, "5", 1, "phụ cấp lưu trú 300.000 đồng mỗi ngày công tác")
U2 = unit(2, 1, "5", 2, "phụ cấp lưu trú trong ngày 150.000 đồng khi đi về trong ngày")
U3 = unit(3, 2, "1", 1, "phụ cấp lưu trú 450.000 đồng mỗi ngày công tác")
U4 = unit(4, 3, "1", 1, "phụ cấp lưu trú 600.000 đồng mỗi ngày công tác sắp tới")
U5 = unit(5, 4, "1", 1, "phụ cấp lưu trú 480.000 đồng mỗi ngày công tác")
U6 = Unit(6, 5, None, "5", "Tiêu đề 5", 1, 1, "Điều 5. Tiêu đề 5\nphụ cấp lưu trú mỗi ngày công tác không rõ ngày")


def run(q, units, amends):
    r = Bm25Retriever()
    r.rebuild(units)
    return resolve(q, r.search(q, 8), units, amends, DOCS, T, r, 0.1, 0.3)


A3 = Amendment(3, "08/2025/QC", "5", 1)


def test_a_clause_superseded_by_in_force_amendment():
    res = run("phụ cấp lưu trú mỗi ngày công tác", [U1, U2, U3], [A3])
    assert res.primary.id == 3 and [u.id for u in res.superseded] == [1]


def test_b_other_clause_not_superseded():
    res = run("phụ cấp lưu trú đi về trong ngày", [U1, U2, U3], [A3])
    assert res.primary.id == 2 and res.superseded == []


def test_c_future_amendment_never_primary():
    res = run("phụ cấp lưu trú mỗi ngày công tác sắp tới", [U1, U4], [Amendment(4, "08/2025/QC", "5", 1)])
    assert res.primary.id == 1 and [u.id for u in res.upcoming] == [4]


def test_d_chain_takes_newest_in_force_and_lists_all_replaced():
    res = run("phụ cấp lưu trú mỗi ngày công tác", [U1, U3, U5], [A3, Amendment(5, "08/2025/QC", "5", 1)])
    assert res.primary.id == 5 and {u.id for u in res.superseded} == {1, 3}


def test_e_unknown_date_never_supersedes():
    res = run("phụ cấp lưu trú mỗi ngày công tác", [U1, U6], [])
    assert res.primary.document_id == 1 or 1 not in [u.document_id for u in res.superseded]


def test_f_only_future_document():
    res = run("phụ cấp lưu trú mỗi ngày công tác sắp tới", [U4], [])
    assert res.primary is None and [u.id for u in res.upcoming] == [4]


def test_below_threshold_is_not_found():
    r = Bm25Retriever()
    r.rebuild([U1, U2])
    q = "thủ đô nước Pháp"
    assert resolve(q, r.search(q, 8), [U1, U2], [], DOCS, T, r, 2.0, 0.5).not_found


def test_no_hits_is_not_found():
    assert resolve("x", [], [], [], DOCS, T, Bm25Retriever(), 2.0, 0.5).not_found
