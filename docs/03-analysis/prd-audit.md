# PRD audit — TCQC-PRD v0.2 (vòng 2)

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-PRD-AUDIT-02 (vòng 1: TCQC-PRD-AUDIT-01, trong git `5eb70a0`) |
| Date | 2026-11-02 |
| Auditor | checklist-auditor sub-agent (audit, không duyệt; PO duyệt) |
| Artifact | `docs/03-analysis/PRD.md` v0.2 + `USER_STORIES.md` v0.2 + `traceability.md` v0.2 (commit `5eb70a0`) |
| Checklist | `sdlc-kit/analysis/PRD_IEEE_29148_Checklist.xlsx` (kit commit `6996dae`), 20 dòng |
| Prompt | `sdlc-kit/analysis/PRD_Prompt_IEEE_standard.md` v2.0 |
| Upstream | `docs/02-requirements/BRD.md` v1.0, tag `requirements-v1` (không khác tag) |

Owner: **Phùng Duy Hùng (PO)**; due **2026-11-02** (CON-01).

## 1. Round 1 → Round 2

| # | Item | V1 | V2 | Lý do |
|---|---|---|---|---|
| 1 | Purpose & Scope | Partial | Pass | §1.3 Scope + boundary |
| 4 | Operating Environment | Partial | Pass | §1.3 trình duyệt, ≥ 1280 px, DEP-004 |
| 5 | Singular & Complete | Partial | Pass | Tách FR-004b, FR-007b, FR-009b |
| 6 | Implementation-Free | Partial | Partial | §5.2 đã sửa; thiết kế mới lọt vào §1.3/§1.4 (xem dưới) |
| 7 | Verifiable | Partial | Pass | FR-015 "quá 30 giây"; OQ-006 ghi đã quyết |
| 8 | Performance & Capacity | Partial (B) | Pass | NFR-002 hết `[Unverified]`; OQ-007 ghi đã quyết |
| 9 | Security & Privacy | Partial | Pass | NFR-009; RSK-004 xử lý ở §1.3 |
| 10 | Reliability & Availability | Partial | Partial | Có % uptime + RPO, nhưng 95 % không có nguồn |
| 11 | Scalability | Partial (B) | Pass | NFR-006 xác nhận; NFR-010 |
| 14 | Software Interfaces | **Fail** | Pass | §1.4 IF-01..IF-04 |
| 15 | Communication Interfaces | Partial | Pass | §1.4: HTTP cục bộ, HTTPS khi triển khai, không kênh ra ngoài |
| 16 | Design Constraints | Partial | Pass | §1.3 CON-01..07, không có quy định pháp lý |
| 17 | Dependencies | **Fail** | Partial (B) | §1.3 có DEP-001..005; quyết định DEP-001 chưa có bản ghi, đổi rủi ro đã baseline |
| 18 | Unambiguous Language | Partial | Pass | §1.1 "≤ 2 phút"; FR-015 30 giây |
| 19 | Traceable & Numbered | Partial | Partial | NFR-005/007 đã giải thích; còn lỗi ID và ma trận cũ |
| 20 | Consistent | Partial | Partial | Đã sửa thông điệp FR-001; phát sinh mâu thuẫn mới |

Không đổi: #2, #3, #12 Pass; #13 N/A.

## 2. Các dòng còn Partial

| # | Item | Evidence | Action | Gate |
|---|---|---|---|---|
| 17 | Dependencies | §1.3 DEP-001: quyết định PO không có bản ghi nguồn (chỉ có `interviews/SRC-005.md`); "RSK-004 không còn áp dụng" đổi BRD §4.10 đã baseline mà không qua C1 | Ghi quyết định PO (OQ-006, OQ-007, DEP-001) vào một SRC/biên bản; ghi việc đóng RSK-004 qua change request cho BRD hoặc ADR | **Blocking** |
| 6 | Implementation-Free | §1.3 "thành phần chạy trong hệ thống, theo quy tắc, hoán đổi được"; IF-04 "các đoạn văn bản tìm được"; §5.2 "số đoạn văn bản đã xét" | Chuyển cách hiện thực sang ADR ở Design; PRD chỉ giữ "không gửi nội dung ra ngoài công ty" | Non-blocking |
| 10 | Reliability & Availability | NFR-005 "≥ 95 %" ghi nguồn ASM-003/ASM-005/OQ-005, nhưng các mục đó không có số 95 % | PO xác nhận 95 % (ghi nguồn) hoặc bỏ | Non-blocking |
| 19 | Traceable & Numbered | ID có hậu tố FR-004b/007b/009b ngoài scheme `FR-xxx` (guide A9); §3.3 thiếu FR-004b, 007b, 009b, 016, 017; traceability "Nguồn: PRD v0.1" | Đặt ID mới FR-018..020 (giữ ID cũ), cập nhật §3.3 và dòng Nguồn | Non-blocking |
| 20 | Consistent | §4.1 "do AI tạo" ≠ §1.3 "theo quy tắc"; FR-002 vẫn có "kho đã đủ 50" trùng FR-016; US-007-AC1/AC2 dùng `latency`, `cited_count`, "CSDL" ≠ §5.2/NFR-003; FR-016/FR-017 được gắn vào US nhưng không có AC nào | Thống nhất nhãn câu trả lời; bỏ lý do 50 khỏi FR-002; cập nhật US-007; thêm AC cho FR-016 (US-001) và FR-017 (US-007) | Non-blocking |

## 3. Tổng kết

| Pass | Partial | Fail | N/A | Tổng |
|---|---|---|---|---|
| 14 | 5 | 0 | 1 | 20 |

**Blocking:** #17 Dependencies (Partial).

## 4. Self-check (§6) và rule của prompt

| Mục | Kết quả |
|---|---|
| OQ có owner và ngày | Đạt (OQ-006, OQ-007: 2026-11-02, Đã quyết) |
| Baseline có giá trị hoặc lý do | Đạt (§1.2) |
| FR/NFR → BR, orphan có giải thích | Đạt (NFR-005, NFR-007: PO chấp nhận, §6) |
| Edge case cho P0 | Đạt (§4.2 thêm FR-016, FR-017) |
| Self-check được báo kèm artifact | Đạt (§6 trỏ tới audit này) |
| §5 giữ cấu trúc, nêu mục được thêm | Vi phạm nhẹ: §1.3/§1.4 đặt trước §1.2; document control không nói đã thêm mục |
| §4 không nêu kiến trúc | Vi phạm (#6) |
| Stop condition: quyết định thiết kế/phạm vi phải được báo cáo, không tự làm | Cần bản ghi quyết định của PO (#17) |

## 5. Verdict

**Not gate ready**: 0 Fail, nhưng còn 1 Partial Blocking (#17). Khi PO có bản ghi nguồn cho các quyết định và ghi việc đóng RSK-004 qua C1/ADR, gói này đủ điều kiện để PO xét duyệt. 4 Partial Non-blocking còn lại có owner và due date. Quyết định duyệt thuộc PO.
