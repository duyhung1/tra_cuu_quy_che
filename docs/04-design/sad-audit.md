# Audit — SAD (TCQC-SAD v0.1) theo SAD_IEEE_1016_Checklist

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-SAD-AUDIT-01 |
| Ngày | 2026-11-02 |
| Auditor | checklist-auditor sub-agent |
| Artifact | `docs/04-design/SAD.md` v0.1 (commit 615f264) + `adr/ADR-001..004` + `diagrams/*.drawio` |
| Checklist | `sdlc-kit/design/SAD_IEEE_1016_Checklist.xlsx` (16 dòng), kit commit `6996dae` |
| Prompt | `sdlc-kit/design/SAD_Prompt_IEEE_standard.md` v2.0; `prompts/04-design.md` (MINIMUM_ADRS = 4) |
| Upstream | PRD/USER_STORIES/traceability/SRC-006 (`analysis-v1`), BRD (`requirements-v1`) |

## 1. Bảng chấm

| # | Category | Checklist Item | Status | Evidence | Notes / Action Items | Owner | Gate |
|---|---|---|---|---|---|---|---|
| 1 | 1. Architecture Context | Scope & Boundary | Pass | §2.1 C4 L1; §3.5 "không có giao diện bên ngoài" (SRC-006 D4) | — | Tech Lead | Non-blocking |
| 2 | 1. Architecture Context | Context View | Pass | §2.1: dịch vụ cung cấp IF-01..03 (khớp PRD §IF); không phụ thuộc dịch vụ ngoài | — | Tech Lead | Non-blocking |
| 3 | 2. Stakeholders & Concerns | Architectural Drivers | Pass | §1.1 bảng 6 driver có nguồn (FR/NFR/BR/SRC-006) và hệ quả kiến trúc | Prompt §7.1.1 yêu cầu "top 3": có thể đánh thứ tự ưu tiên | Tech Lead | Non-blocking |
| 4 | 2. Stakeholders & Concerns | System Constraints | Partial | §1.2 CON-01..07, DEP-004; NFR-009 được map tới §4.1/§4.5 nhưng §4.1 không nói gì về mã hóa | Thêm 1 dòng vào §4.1: NFR-009 N/A capstone (CON-02), khi dùng thật HTTPS + mã hóa nơi lưu. Due 2026-11-03 | Tech Lead | Non-blocking |
| 5 | 3. Structural Viewpoints | Composition View | Pass | §2.2 CMP-01..09, mỗi CMP có trách nhiệm, interface, FR/NFR; `component.drawio` khớp 9 CMP | — | Tech Lead | Non-blocking |
| 6 | 3. Structural Viewpoints | Logical View | Pass | §3.1 ER DOCUMENT/UNIT/AMENDMENT/ASK_LOG; kiểu dữ liệu ở blueprint §3 | — | Tech Lead | Non-blocking |
| 7 | 4. Behavioral Viewpoints | Dependency View | Pass | §2.3 sơ đồ + quy tắc `api → services → domain/ports ← adapters`, thư viện ngoài nêu tên | — | Tech Lead | Non-blocking |
| 8 | 4. Behavioral Viewpoints | Interaction View | Partial | §3.2/§3.3 có từng bước + lỗi; `sequence-ask.drawio` bước 9 trả `{answer, sources}` thiếu `latency_ms`/`found` (SAD §3.3.7, blueprint API-03); `sequence-ingest.drawio` thiếu `collection_full` và nhánh `failed`/rollback | Đồng bộ sơ đồ với §3.2/§3.3 và blueprint §5. Due 2026-11-03 | Tech Lead | Non-blocking |
| 9 | 4. Behavioral Viewpoints | State Dynamics View | Pass | §3.4 `processing → ready \| failed`, ràng buộc ADR-004 | — | Tech Lead | Non-blocking |
| 10 | 5. Data & Interface Viewpoints | Information View | Pass | §3.1 ER + blueprint §4; §4.2 ASK_LOG chỉ cột số (NFR-003) | Chưa nêu chính sách lưu giữ dữ liệu (prompt §7.2.3) — xem §2 | Tech Lead | Non-blocking |
| 11 | 5. Data & Interface Viewpoints | Interface View | Partial | §3.5 → blueprint §5 (API-01..03, mã lỗi). PRD IF-01 trả trạng thái "Đang xử lý", SAD/ADR-004 trả trạng thái cuối `ready/failed` — lệch hợp đồng IF-01 chưa ghi OQ | Ghi lệch IF-01 vào §7 (OQ) hoặc nêu rõ trong ADR-004 là thay đổi có PO chấp thuận. Due 2026-11-03 | PO | Non-blocking |
| 12 | 6. Deployment & Resources | Resource View | Pass | §4.4 bảng tài nguyên (kho, chỉ mục, CPU/RAM, đồng thời) | — | Tech Lead | Non-blocking |
| 13 | 6. Deployment & Resources | Physical/Execution Mapping | Pass | §4.5 node → CMP-01..09, tệp `data/tcqc.db` | — | Tech Lead | Non-blocking |
| 14 | 7. Design Rationale (ADR) | Architectural Decisions | Pass | §6 index; ADR-001..004 đủ Bối cảnh/Quyết định/Hệ quả; 4 ≥ MINIMUM_ADRS | — | Tech Lead | Non-blocking |
| 15 | 7. Design Rationale (ADR) | Rejected Alternatives | Pass | Mỗi ADR có bảng "Lựa chọn đã xét" 2–3 phương án có lý do | — | Tech Lead | Non-blocking |
| 16 | 7. Design Rationale (ADR) | Traceability | Pass | ADR "Liên quan" dẫn FR/NFR/BR/RSK; §5 map đủ FR-001..020, NFR-001..010 (đã đối chiếu PRD) | — | Tech Lead | Non-blocking |

## 2. Prompt self-check (§6) và vi phạm §4/§5/§7

| Mục | Kết quả |
|---|---|
| Drivers trước thiết kế | Đạt (§1.1) |
| Mọi component trace FR/NFR + interface | Đạt (§2.2) |
| Flow quan trọng có từng bước + lỗi | Đạt (§3.2, §3.3) |
| Security, data protection, reliability, observability | Đạt một phần: §4.1–4.3 có, nhưng thiếu mã hóa at-rest/in-transit (NFR-009) và rate-limiting/retry (prompt §7.4.2) |
| ≥ 4 ADR | Đạt (4) |
| Vi phạm: §5 "Follow the four-part structure of §7 and its sub-headings" | §2 dùng Context/Components/Dependency thay cho 2.1 Frontend / 2.2 Application / 2.3 Data infra / 2.4 Backend API; chấp nhận được vì nội dung tương đương, nhưng thiếu data retention (2.3) |
| Vi phạm: §3 bước 6 "report the score with the document" | SAD không kèm điểm self-check |
| Sơ đồ `.drawio` | Cả 3 tệp là XML `mxfile` hợp lệ (1 diagram, 1 mxGraphModel, 9–10 edge), chỉnh sửa được; component khớp SAD, sequence lệch nhỏ (dòng 8) |
| ID upstream | DEP-004, ASM-005, OQ-002, BRU-001..003, BR-011/012/014, CON-07, IF-01..03, MET-002/003, RSK-003/005, SRC-006 D4/D5 đều tồn tại upstream |

## 3. Tổng hợp

| Pass | Partial | Fail | N/A |
|---|---|---|---|
| 13 | 3 | 0 | 0 |

**Blocking items:** không có.

**Partial (Non-blocking):** #4 System Constraints (NFR-009 chưa nêu ở §4.1); #8 Interaction View (sequence diagrams lệch payload/nhánh lỗi); #11 Interface View (lệch IF-01 "Đang xử lý" vs xử lý đồng bộ, chưa ghi OQ).

## 4. Verdict

**Gate ready** (0 Fail). Đề nghị sửa 3 Partial trước khi PO duyệt; auditor không phê duyệt — PO phê duyệt.
