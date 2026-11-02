# PRD audit — TCQC-PRD v0.3 (vòng 3, vòng cuối)

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-PRD-AUDIT-03 (vòng 1: `5eb70a0`; vòng 2: `617a1a1`) |
| Date | 2026-11-02 |
| Auditor | checklist-auditor sub-agent (audit, không duyệt; PO duyệt) |
| Artifact | `docs/03-analysis/PRD.md` v0.3 + `USER_STORIES.md` v0.3 + `traceability.md` v0.3 + `decisions/SRC-006.md` (commit `617a1a1`) |
| Checklist | `sdlc-kit/analysis/PRD_IEEE_29148_Checklist.xlsx` (kit commit `6996dae`), 20 dòng |
| Prompt | `sdlc-kit/analysis/PRD_Prompt_IEEE_standard.md` v2.0 |
| Upstream | `docs/02-requirements/BRD.md` v1.0, tag `requirements-v1` (không khác tag) |

Owner: **Phùng Duy Hùng (PO)**; due **2026-11-02** (CON-01).

## 1. Round 2 → Round 3

| # | Item | V2 | V3 | Evidence |
|---|---|---|---|---|
| 6 | Implementation-Free | Partial | Pass | §1.3 DEP-001: "cách tạo câu trả lời được quyết ở ADR"; §5.2 bỏ "số đoạn" |
| 17 | Dependencies | Partial (B) | Pass | SRC-006 D1–D4 ghi quyết định; RSK-004 vẫn mở, BRD không đổi (SRC-006 cuối trang, §1.3) |
| 19 | Traceable & Numbered | Partial | Pass | FR-018/019/020; §3.3 đủ FR; traceability "Nguồn: PRD v0.3" |
| 10 | Reliability & Availability | Partial | Partial | Đã bỏ 95 % không nguồn; giờ không còn cam kết % uptime nào |
| 20 | Consistent | Partial | Partial | Các lỗi vòng 2 đã sửa (§4.1, FR-002, US-001-AC6, US-007-AC1..4); có 2 mâu thuẫn mới từ SRC-006 |

Không đổi: 15 dòng Pass, #13 Hardware Interfaces N/A.

## 2. Các dòng còn Partial

| # | Item | Evidence | Action | Gate |
|---|---|---|---|---|
| 10 | Reliability & Availability | NFR-005 "Dùng được trong giờ 08:00–17:30" — có khung giờ, RTO, RPO nhưng không có % uptime | Ghi rõ "không cam kết % uptime trong capstone (ASM-003)" hoặc PO chọn một con số qua SRC | Non-blocking |
| 20 | Consistent | (a) SRC-006 D4 (adapter giả) + D5 (không có khóa API) ≠ RC-2: chưa nói golden set MET-002..004 được đo trên thành phần nào; (b) SRC-006 D7 (agent tự baseline cổng 3–6) ≠ BRD CON-07 "Agent không tự duyệt hay baseline" mà §1.3 nói là áp dụng | (a) Thêm RSK/OQ: RC-2 đo trên adapter giả thì chỉ chứng minh luồng, không chứng minh chất lượng; (b) PO đổi CON-07 qua C1 hoặc rút lại D7 trước cổng 3 | Non-blocking cho cổng PRD; (b) phải xong trước cổng 3 |

## 3. Tổng kết

| Pass | Partial | Fail | N/A | Tổng |
|---|---|---|---|---|
| 17 | 2 | 0 | 1 | 20 |

**Blocking:** không có.

## 4. Self-check (§6) và rule của prompt

| Mục | Kết quả |
|---|---|
| Objectives có baseline/lý do, target, cách đo | Đạt (§1.2, đã về đúng thứ tự) |
| FR/NFR → BR; orphan có giải thích | Đạt (20 FR, 10 NFR; NFR-005/007 PO chấp nhận) |
| US có AC và FR | Đạt (10/10; FR-016 → US-001-AC6, FR-017 → US-007-AC4) |
| NFR có ngưỡng và cách đo | Đạt (NFR-005 xem #10) |
| Edge case cho P0 | Đạt (§4.2) |
| Release criteria đo được | Đạt về hình thức; ý nghĩa của RC-2 khi dùng adapter giả: #20 (a) |
| §5 cấu trúc, khai báo mục thêm | Đạt (document control "Thay đổi 0.3") |
| Quyết định có nguồn mở được | Đạt (SRC-006; người ghi là agent, PO xác nhận khi tự đọc PRD theo D6) |

## 5. Verdict

**Gate ready**: 0 Fail, 0 Blocking. 2 Partial Non-blocking có owner và due date; #20 (b) (D7 so với CON-07) cần PO xử lý trước cổng 3. Theo SRC-006 D6, PO tự đọc PRD trước khi duyệt. Auditor không duyệt.

## Quyết định tại cổng (2026-11-02)

PO đọc PRD v0.3 và duyệt (SRC-006 D9). Partial #10 và #20(a) được ghi vào PRD v1.0 (NFR-005, RSK-005). #20(b) được giải quyết bằng SRC-006 D8: rút D7, PO duyệt từng cổng. Baseline `analysis-v1`.
