# PRD audit — TCQC-PRD v0.1 (vòng 1)

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-PRD-AUDIT-01 |
| Date | 2026-11-02 |
| Auditor | checklist-auditor sub-agent (audit, không duyệt; PO duyệt) |
| Artifact | `docs/03-analysis/PRD.md` v0.1 + `USER_STORIES.md` v0.1 + `traceability.md` v0.1 (gói Analysis) |
| Checklist | `sdlc-kit/analysis/PRD_IEEE_29148_Checklist.xlsx` (kit commit `6996dae`), 20 dòng |
| Prompt | `sdlc-kit/analysis/PRD_Prompt_IEEE_standard.md` v2.0 (§6 self-check, §2.3–§5 rules) |
| Upstream | `docs/02-requirements/BRD.md` v1.0, tag `requirements-v1` (đã kiểm: không khác tag) |

Owner mặc định: **Phùng Duy Hùng (PO)** — người duy nhất có quyền sửa/duyệt; due **2026-11-02** (CON-01).

## 1. Bảng chấm

| # | Category | Checklist Item | Status | Evidence | Notes / Action Items | Owner | Gate |
|---|---|---|---|---|---|---|---|
| 1 | 1. Introduction & Context | Purpose & Scope | Partial | §1.1 chỉ có vision; không có mục scope/boundary/out-of-scope (BRD §4.5) | Thêm mục Scope: in/out/deferred và boundary, tham chiếu BRD §4.5 | PO, 2026-11-02 | Non-blocking |
| 2 | 1. Introduction & Context | Business Context | Pass | §0 pillars ↔ BR; §1.2 OKR ↔ MET-001..004, 006 | (Ghi chú) BO-004/MET-007 không có KR dù FR-007 dùng MET-007 | — | Non-blocking |
| 3 | 2. Stakeholders & Environment | User Characteristics | Pass | §2.1: 3 persona ↔ STK-02..04, mức hiểu quy chế, ưu tiên | (Ghi chú) "PO" dùng trong US-007/US-008 nhưng không có trong §2.1 | — | Non-blocking |
| 4 | 2. Stakeholders & Environment | Operating Environment | Partial | Chỉ NFR-004 (mạng nội bộ); thiếu trình duyệt/máy tính (BRD §4.6, DEP-004) | Thêm mục môi trường: trình duyệt trên máy tính trong mạng công ty, máy cục bộ giả lập | PO, 2026-11-02 | Non-blocking |
| 5 | 3. Functional Requirements | Singular & Complete | Partial | FR-007 (chỉ dùng Sẵn sàng + [n]), FR-009 (BR-006 + BR-007), FR-004 (hiển thị + tự cập nhật) gộp nhiều nghĩa vụ | Tách FR-007, FR-009, FR-004 thành yêu cầu đơn; giữ ID cũ, thêm ID mới | PO, 2026-11-02 | Non-blocking |
| 6 | 3. Functional Requirements | Implementation-Free | Partial | §5.2 `chunk_count`, "token vào/ra", "số đoạn"; NFR-003 "CSDL" | Thay bằng thuật ngữ hành vi hoặc dời sang Design | PO, 2026-11-02 | Non-blocking |
| 7 | 3. Functional Requirements | Verifiable | Partial | FR-015 "quá thời gian" không có ngưỡng; FR-007 dựa MET-007 còn `[Unverified: OQ-006]` | Đặt ngưỡng timeout cho FR-015; đóng OQ-006 trước chặng Test | PO, 2026-11-02 | Non-blocking |
| 8 | 4. Non-Functional Requirements | Performance & Capacity | Partial | NFR-002 `[Unverified: OQ-007]`; OQ-007 "Cần trước: Cổng PRD" vẫn Mở | PO xác nhận hoặc sửa ngưỡng NFR-002, đóng OQ-007 | PO, 2026-11-02 | **Blocking** |
| 9 | 4. Non-Functional Requirements | Security & Privacy | Partial | NFR-003, NFR-004, NFR-008 (không RBAC, có lý do); không nói mã hóa lưu trữ, không xử lý RSK-004 (gửi nội dung ra DEP-001) | Thêm NFR về mã hóa (hoặc ghi rõ không áp dụng, CON-02) và ràng buộc dịch vụ ngoài theo RSK-004 | PO, 2026-11-02 | Non-blocking |
| 10 | 4. Non-Functional Requirements | Reliability & Availability | Partial | NFR-005: khung giờ + RTO ≤ 1 ngày; không có % uptime, không ghi RPO (ASM-005) | Thêm % sẵn sàng trong giờ hành chính (hoặc ghi "best effort" có PO chấp nhận) và RPO | PO, 2026-11-02 | Non-blocking |
| 11 | 4. Non-Functional Requirements | Scalability | Partial | NFR-006 `[Unverified: OQ-007]`; giới hạn 50 văn bản chỉ nằm trong FR-002 | Đóng OQ-007; nêu sức chứa 50 văn bản/300 trang thành NFR | PO, 2026-11-02 | **Blocking** |
| 12 | 5. Interface Requirements | User Interfaces (UI) | Pass | §4.1 hai màn hình, tương tác logic; §4.2 trạng thái lỗi | — | — | Non-blocking |
| 13 | 5. Interface Requirements | Hardware Interfaces | N/A | Ứng dụng web trên máy tính; không có thiết bị ngoại vi (BRD §4.6) | — | — | Non-blocking |
| 14 | 5. Interface Requirements | Software Interfaces | **Fail** | Không có mục interface; DEP-001 (dịch vụ hiểu ngôn ngữ) không xuất hiện trong PRD/US/traceability | Thêm mục Software Interfaces ở mức logic: dịch vụ tạo câu trả lời (vào/ra, lỗi → FR-015), đầu vào PDF | PO, 2026-11-02 | **Blocking** |
| 15 | 5. Interface Requirements | Communication Interfaces | Partial | NFR-004 "HTTPS khi triển khai" — không rõ có áp dụng cho bản chạy cục bộ (DEP-004); kênh tới DEP-001 không nêu | Ghi rõ HTTPS áp dụng ở môi trường nào và kênh tới dịch vụ ngoài | PO, 2026-11-02 | Non-blocking |
| 16 | 6. Constraints & Assumptions | Design Constraints | Partial | Chỉ CON-04 (NFR-007); thiếu CON-01..03, 05..07 và REGULATORY_CONTEXT "none" (`prompts/03-analysis.md`) | Thêm mục Constraints tham chiếu BRD §4.9 và ghi "không có quy định pháp lý" | PO, 2026-11-02 | Non-blocking |
| 17 | 6. Constraints & Assumptions | Dependencies | **Fail** | Không có DEP-001..005 trong gói (grep `DEP-` = 0 kết quả) | Thêm mục Dependencies liệt kê DEP-001..005 và FR/NFR bị ảnh hưởng | PO, 2026-11-02 | **Blocking** |
| 18 | 7. Requirements Quality Check | Unambiguous Language | Partial | §1.1 "tra được trong vài giây" ≠ KR2 p90 ≤ 30 giây; FR-015 "quá thời gian" | Sửa vision cho khớp MET-001/006; định lượng timeout | PO, 2026-11-02 | Non-blocking |
| 19 | 7. Requirements Quality Check | Traceable & Numbered | Partial | NFR-005 (ASM), NFR-007 (CON-04) không có BR, không đánh `[ORPHAN]`/OQ; traceability dòng BR-002 thiếu US-002 (FR-004) | Đánh dấu và mở OQ cho NFR-005/007 hoặc PO chấp nhận ghi rõ; sửa dòng BR-002 | PO, 2026-11-02 | Non-blocking |
| 20 | 7. Requirements Quality Check | Consistent | Partial | FR-001 lý do "quá 10 tệp" ≠ US-001-AC2 "Mỗi lần chỉ tải tối đa 10 tệp"; §4.2 "từ chối trước khi gửi" ≠ US-001-AC2 "When: gửi"; vision ≠ KR2 | Thống nhất thông điệp và thời điểm từ chối; sửa vision | PO, 2026-11-02 | Non-blocking |

## 2. Tổng kết

| Pass | Partial | Fail | N/A | Tổng |
|---|---|---|---|---|
| 3 | 14 | 2 | 1 | 20 |

**Blocking:** #14 Software Interfaces (Fail), #17 Dependencies (Fail), #8 Performance & Capacity (Partial, OQ-007), #11 Scalability (Partial, OQ-007).

## 3. Self-check (§6) và rule của prompt

| Mục | Kết quả | Evidence |
|---|---|---|
| §3.6/§6: báo điểm self-check kèm artifact | Vi phạm | PRD không có điểm checklist nào |
| §5: OQ có owner **và ngày** | Vi phạm | OQ-006 "Trước chặng Test", OQ-007 "Cổng PRD" — không có ngày |
| §6: mọi objective có baseline | Partial | KR2–KR5 baseline "—" không ghi lý do (BRD §4.4 có lý do) |
| §6: 100 % FR/NFR → BR, không orphan chưa giải thích | Vi phạm | NFR-005, NFR-007 (xem #19) |
| §6: 100 % US có AC và FR | Đạt | US-001..010 đều có AC, FR; P0 đều có GWT, ≤ 5 AC |
| §6: mọi NFR có ngưỡng và cách đo | Đạt (2 ngưỡng chưa xác nhận) | NFR-001..008; NFR-002/006 `[Unverified]` |
| §6: edge case cho mỗi P0 | Partial | Thiếu: kho đủ 50 văn bản (FR-002) trong §4.2 và US-001; lỗi ghi số liệu (FR-014) |
| §6: release criteria đo được | Đạt | §5.1 RC-1..6 |
| §6 stop condition: OQ chặn gate còn mở | Vi phạm | OQ-007 cần trước Cổng PRD, đang Mở |
| §4: không nêu kiến trúc | Vi phạm nhẹ | §5.2 chunk/token (xem #6) |
| §2.1 IN-2: glossary, stakeholders là input bắt buộc | Vi phạm nhẹ | Document control chỉ ghi BRD |

## 4. Verdict

**Not gate ready** — 2 Fail (#14, #17) và 2 Partial Blocking (#8, #11 do OQ-007). Cần PRD v0.2 và audit vòng 2. Quyết định duyệt thuộc PO.
