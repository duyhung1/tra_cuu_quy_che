# Audit — Blueprint (SDD) TCQC — vòng 2

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-SDD-AUDIT-02 |
| Date | 2026-11-02 |
| Auditor | checklist-auditor sub-agent |
| Artifact | `docs/04-design/blueprint.md` v0.2 (commit `ab1c475`, nhánh `restart`), đọc kèm `SAD.md` v0.2, `adr/ADR-001..004`, `diagrams/` |
| Checklist | `sdlc-kit/design/BluePrint_Design_IEEE_1016_2009_Checklist.xlsx` (19 dòng); prompt `sdlc-kit/design/bluePrint_design_prompt.md` v2.0; kit commit `ab1c475` |
| Upstream | `analysis-v1`: PRD v1.0 (FR-001..020, NFR-001..010), USER_STORIES (US-004/005/006/008), SRC-006; BRD `requirements-v1` (BRU-001..003, AC-007/012/013/015) |
| Vòng trước | TCQC-SDD-AUDIT-01 trên v0.1 (commit `615f264`; bản audit được commit ở `ab1c475`): 14 Pass / 4 Partial / 1 Fail |

Agent không duyệt; PO duyệt. Audit không sửa artifact.

## 1. Round 1 → Round 2

| # | Item | Vòng 1 | Vòng 2 | Căn cứ thay đổi |
|---|---|---|---|---|
| 4 | Design Concerns | Partial | **Pass** | §1 bảng concern → view; QS-1..4 có phản hồi đo được |
| 6 | Logical View | Partial | **Pass** | §3 thêm `PageText`, `IngestResult`, `AskResult`, bảng port gồm `PdfExtractor`, `DocumentStore`, `Clock` |
| 10 | Interface View | Partial | Partial | Đã có thân lỗi `{code, message}`, trim câu hỏi, `found` ở SAD §3.3 bước 7. Còn I1 |
| 12 | Algorithm View | **Fail (Blocking)** | Partial (Non-blocking) | A1–A10 đã xử lý (§2); còn R1–R5 là trường hợp biên |
| 19 | Completeness Check | Partial | Partial | Banner FR-005 đã thêm ở §7 nhưng dựa vào trường API không có (I1); R1–R5 |

## 2. Kiểm lại A1–A10 (vòng 1)

| ID | Vòng 2 | Bằng chứng |
|---|---|---|
| A1 future amendment áp dụng sớm | Đã sửa | §6.5 bước 1 tách `current`/`future`, `h0` chỉ lấy từ `current`; bước 5 "không unit nào trong upcoming được làm primary"; test (c) |
| A2 nhiều amendment / chuỗi | Đã sửa | §6.5 bước 4: vòng lặp ≤ 5, chọn `eff` lớn nhất, tie-break `signed_date` rồi `id`; test (d) |
| A3 `effective_date` NULL | Đã sửa | §6.2 `eff(D)`: fallback `signed_date`, rồi −∞, "không bao giờ thay thế"; test (e) |
| A4 regex ngày hiệu lực | Đã sửa | §6.2 ba mẫu `\s+` đúng, có dạng "ngày … tháng … năm", "kể từ ngày ký" |
| A5 IGNORECASE / NFC | Đã sửa | §6.0 |
| A6 định dạng sửa đổi, số hiệu | Đã sửa | §6.0 `DOC_NO` dùng chung + chuẩn hóa gạch ngang; §6.3 bước 1–4 (gồm "sửa đổi, bổ sung", tập `K(N)`, dòng NULL) |
| A7 điểm unit ngoài top-k | Đã sửa | §6.5 định nghĩa `score(q, u)` cho mọi unit; port `Retriever.score` |
| A8 ngưỡng sau khi đổi primary, IDF, hiệu chỉnh τ | Đã sửa | §6.5 bước 2 `found_score = score(h0)`; §6.4 công thức IDF; §6.7 τ cấu hình, hiệu chỉnh và ghi ở TEST_REPORT |
| A9 stop-word, bigram | Đã sửa | §6.4 danh sách đóng, nguồn duy nhất `text.py`; thứ tự bigram |
| A10 định nghĩa "câu" | Đã sửa | §6.0; §6.6 lọc theo câu |

## 3. Bảng chấm vòng 2

| # | Category | Checklist Item | Status | Evidence | Notes / Action Items | Owner | Gate |
|---|---|---|---|---|---|---|---|
| 1 | 1. Context & Subject | Design Subject Scope | Pass | §1; SAD §2.1, §1.1 | — | PO / Tech Lead | Non-blocking |
| 2 | 1. Context & Subject | Context View | Pass | SAD §2.1, §3.5 | — | PO / Tech Lead | Non-blocking |
| 3 | 2. Stakeholders & Concerns | Stakeholder Identification | Pass | §1 (PO/Tech Lead, AI agent, HC-NS, STK-02..04) | — | PO / Tech Lead | Non-blocking |
| 4 | 2. Stakeholders & Concerns | Design Concerns | Pass | §1 bảng concern → view; QS-1..4 dẫn NFR-001/002/003/006, FR-012 | — | PO / Tech Lead | Non-blocking |
| 5 | 3. Design Views | Composition View | Pass | §2 | — | PO / Tech Lead | Non-blocking |
| 6 | 3. Design Views | Logical View | Pass | §3 kiểu + bảng port | Nhỏ: dòng `Resolution` ở §3 chưa khớp §6.5 bước 7 (`primary` có thể None; có `found_score`, `matched_terms`). Cập nhật khi sửa I1 | PO / Tech Lead | Non-blocking |
| 7 | 3. Design Views | Dependency View | Pass | SAD §2.3; §2 `wiring.py`; port `PdfExtractor` đóng lỗ hổng vòng 1 | — | PO / Tech Lead | Non-blocking |
| 8 | 3. Design Views | Interaction View | Pass | SAD §3.2, §3.3; `diagrams/sequence-*.drawio` | — | PO / Tech Lead | Non-blocking |
| 9 | 3. Design Views | Information View | Pass | §4 DDL; khóa số hiệu chuẩn hóa ở §6.0 | — | PO / Tech Lead | Non-blocking |
| 10 | 3. Design Views | Interface View | Partial | §5 API-01..04, thân lỗi, trim. **I1:** §7 dùng `counts.processing`, nhưng API-02 chỉ trả `counts:{ready, failed, total}` | Thêm `processing` vào `counts` của API-02. Hạn 2026-11-02 | PO / Tech Lead | Non-blocking |
| 11 | 3. Design Views | State Dynamics View | Pass | §6.8 → SAD §3.4 | — | PO / Tech Lead | Non-blocking |
| 12 | 3. Design Views | Algorithm View | Partial | §6.0–§6.7; A1–A10 đã sửa (§2); test bắt buộc (a)–(f) ở §6.5. Còn R1–R5 (§4) | Sửa R1, R2 (nên làm trước khi viết TASK-007); R3–R5 tùy chọn. Hạn 2026-11-02 | PO / Tech Lead | Non-blocking |
| 13 | 4. Design Elements | Element Attributes | Pass | §2; SAD §2.2 | — | PO / Tech Lead | Non-blocking |
| 14 | 4. Design Elements | Resource Allocation | Pass | §8 → SAD §4.4 | — | PO / Tech Lead | Non-blocking |
| 15 | 5. Design Rationale | Decision Documentation | Pass | §9 → ADR-001..004 | — | PO / Tech Lead | Non-blocking |
| 16 | 5. Design Rationale | Alternatives Considered | Pass | Bảng phương án trong ADR-001..004 | — | PO / Tech Lead | Non-blocking |
| 17 | 5. Design Rationale | Assumptions & Constraints | Pass | §9; SAD §1.2; §6.7 τ là giả định cần hiệu chỉnh | — | PO / Tech Lead | Non-blocking |
| 18 | 6. Traceability & QA | Requirements Traceability | Pass | §10 phủ FR-001..020, NFR-001..010; §1 concern → view | — | PO / Tech Lead | Non-blocking |
| 19 | 6. Traceability & QA | Completeness Check | Partial | Mọi FR/NFR có phần tử; FR-005 banner ở §7. Còn I1 (banner không có dữ liệu) và R1 (rủi ro cho FR-011) | Đóng cùng I1, R1. Hạn 2026-11-02 | PO / Tech Lead | Non-blocking |

## 4. Còn lại trong §6 (Non-blocking)

- **R1 — §6.5 bước 2 / §6.7 (FR-011):** nhánh `current` rỗng trả "Hiện chưa có quy định đang áp dụng." với `found = true` mà không áp ngưỡng τ. Một câu âm tính mà mọi hit đều thuộc văn bản tương lai sẽ không ra NOT_FOUND. **Sửa:** áp ngưỡng §6.7 bước 1 lên `future[0]` trước khi vào nhánh này; ghi rõ hit có điểm 0 bị loại khỏi `hits`.
- **R2 — §6.5 bước 1–3 (FR-010):** bước 1 bỏ hit tương lai trước khi tìm gốc, nên khi hit tốt nhất là Khoản sửa đổi chưa hiệu lực, `h0 = current[0]` có thể là một unit không liên quan nếu Khoản cũ không lọt top-k. Lúc đó bản sửa đổi tương lai cũng không vào `upcoming`, vì bước 5 chỉ xét `amenders(applied/base)`. **Sửa:** với `h ∈ future` có `targets(h.unit)`, thay bằng đích đang hiệu lực, chấm bằng `score(q, t)`, trước khi chọn `h0`. Test (c) nên dựng thêm ca Khoản cũ ngoài top-k.
- **R3 — §6.5 bước 4 (FR-020):** khi B và C cùng sửa một đích, chỉ C được giữ còn B không vào `superseded`, nên câu trả lời nêu mức của bản gốc chứ không nêu mức vừa bị thay. Cần ghi đây là hành vi được chấp nhận, hoặc đưa B vào `superseded`.
- **R4 — §6.0 / §6.6:** "câu" kết thúc ở `.`, nên số "300.000", "1.000.000.000" bị cắt giữa chừng. Nếu câu chỉ dẫn chứa số có dấu chấm, chỉ một mảnh câu bị loại. **Sửa:** không tách ở `.` nằm giữa hai chữ số.
- **R5 — §6.2:** "lần xuất hiện đầu tiên … theo thứ tự ưu tiên" có thể hiểu hai cách (vị trí trước, hay mẫu trước). Văn bản sửa đổi thường nhắc ngày hiệu lực của văn bản bị sửa trước ngày của chính nó. Nên ưu tiên Điều có tiêu đề chứa "hiệu lực".

Đánh giá: đến v0.2, thuật toán FR-009, FR-010, FR-011, FR-012 đã đặc tả đủ để triển khai và kiểm thử với bộ văn bản mẫu tự soạn (DEP-002). R1–R5 là trường hợp biên, cách sửa đã rõ.

## 5. Self-check của prompt và output contract

| Mục | Kết quả |
|---|---|
| Concern → view | Đạt (§1) |
| Tám view, nhất quán | Đạt; lệch nhỏ: `Resolution` (#6), `counts.processing` (I1) |
| Không có element mồ côi | Đạt (§10) |
| QA scenario đo được | Đạt (QS-1..4) |
| Không placeholder / không mâu thuẫn SAD | Không placeholder. Header "Đầu vào: SAD v0.1" đã cũ, SAD hiện là v0.2: cần cập nhật |
| Danh sách OQ, điểm self-check | Đạt (§11: OQ-008, self-check, trỏ tới audit này) |
| Thứ tự section theo §7 | Vẫn chưa có UX/UI scenario và constraints (§7.2.4–2.5); không chặn |

## 6. Tổng hợp

| Pass | Partial | Fail | N/A |
|---|---|---|---|
| 16 | 3 | 0 | 0 |

**Blocking:** không có.

**Partial (Non-blocking, Owner PO / Tech Lead, hạn 2026-11-02):** #10 Interface View (I1), #12 Algorithm View (R1–R5), #19 Completeness Check (I1, R1).

**Verdict: Gate ready.** Có 0 Fail và 0 Blocking. PO duyệt tại cổng Design, gồm cả OQ-008. Nên sửa I1, R1, R2 trước khi giao TASK-007.


## Quyết định tại cổng (2026-11-02)

PO duyệt có điều kiện; điều kiện đạt ở vòng 2 (0 Fail, 0 Blocking). Trước khi baseline đã sửa thêm I1, R1, R2, R3, R4, R5 theo khuyến nghị của auditor. OQ-008 được PO chấp nhận. Baseline `design-v1`.
