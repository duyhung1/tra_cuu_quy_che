# Audit — Software Development Plan, WBS, TASK-001..012

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-SDP-AUDIT-01 |
| Ngày | 2026-11-02 |
| Auditor | checklist-auditor sub-agent |
| Artifact | `Software_Development_Plan.md` v0.1, `WBS.md` v0.1, `tasks/TASK-001..012.md` (commit `01f28e1`) |
| Checklist | `sdlc-kit/development/DevPlan_ISO_24748_5_Checklist.xlsx` (22 mục), kit commit `6996dae` |
| Prompt | `DevPlan_ISO_24748_5_Prompt.md` §6, §7.3; `TaskBreakdown_ISO_21511_Prompt.md` §7.2 3.4 |
| Upstream | `docs/03-analysis` (`analysis-v1`), `docs/04-design` (`design-v1`) |

## 1. Bảng chấm

| # | Checklist Item | Status | Evidence | Notes / Action Items | Owner | Gate |
|---|---|---|---|---|---|---|
| 1 | Project Purpose & Scope | Pass | SDP §1 (FR-001..020, NFR-001..010, PRD §1.3); WBS §1 | — | PO | Non-blocking |
| 2 | Business Drivers & Objectives | Pass | SDP §1 BO-001..004 (BRD §4.4) | — | PO | Non-blocking |
| 3 | System & Software Context | Pass | SDP §1 → SAD §2.1, SRC-006 D4 | — | Tech Lead | Non-blocking |
| 4 | Applicable Standards & Compliance | Partial | SDP §1 Standards: 24748-5, 21511, 1028, 829 | Ghi rõ 12207/27001 áp dụng hay không (kèm lý do); thêm nghĩa vụ tuân thủ (dữ liệu giả lập CON-02). Due 2026-11-02 | PO | Non-blocking |
| 5 | Software Lifecycle Model | Pass | SDP §2 Incremental, W1–W3 | — | PO | Non-blocking |
| 6 | Development Processes & Activities | Pass | SDP §2 quy trình mỗi task; §6.2 cổng | — | Tech Lead | Non-blocking |
| 7 | Process Tailoring & Adaptation | Pass | SDP §2 Tailoring (vai trò gộp, không CI từ xa) | Xem vi phạm P-1 (cấu trúc §7.3 bị rút gọn nhưng không ghi là tailoring) | PO | Non-blocking |
| 8 | Deliverables & Work Products | Pass | SDP §2 DEL-1..6; WBS §2 bảng deliverable | — | PO | Non-blocking |
| 9 | Roles & Responsibilities | Pass | SDP §3; WBS §4 RACI | — | PO | Non-blocking |
| 10 | Governance & Oversight Structure | Pass | SDP §3 Governance (cổng mỗi chặng, CON-07) | — | PO | Non-blocking |
| 11 | Stakeholder Management | Pass | SDP §3 STK-01..05 (BRD có 11 tham chiếu STK) | — | PO | Non-blocking |
| 12 | Estimation Methods & Metrics | Partial | SDP §4; WBS §2 tổng 8,75 giờ, "theo kinh nghiệm", Medium | Không có dữ liệu lịch sử/mô hình; ghi giả định ước lượng và biên độ (vd. ±50 %) kèm RSK-006. Due 2026-11-02 | PO | Non-blocking |
| 13 | Human Resources & Competencies | Partial | SDP §4 "1 PO, 1 AI agent" | Thiếu kỹ năng yêu cầu (PyMuPDF, FastAPI, IEEE 1028) và cách bù khi thiếu. Due 2026-11-02 | PO | Non-blocking |
| 14 | Infrastructure & Tooling | Pass | SDP §4 Hạ tầng; §6.2 lệnh cụ thể | — | Tech Lead | Non-blocking |
| 15 | Budget & Financial Plan | Pass | SDP §4 Ngân sách (BRD §4.2, chi phí ngoài 0) | — | PO | Non-blocking |
| 16 | Schedule & Milestone Baseline | Partial | SDP §5: MS-1..4 cùng ngày 2026-11-02, không giờ; Status "In review" | Thêm mốc giờ hoặc thứ tự kiểm tra được cho MS-2..4; phê duyệt baseline tại cổng `plan-v1`. Due 2026-11-02 | PO | Non-blocking |
| 17 | Progress Tracking & Reporting | Partial | SDP §5 Theo dõi tiến độ (status front-matter, commit) | Không có KPI/tần suất báo cáo; thêm ít nhất: số task done/12, giờ thực tế vs ước lượng, báo cáo sau mỗi wave. Due 2026-11-02 | PO | Non-blocking |
| 18 | Risk & Issue Management | Partial | SDP §5 Rủi ro RSK-001/002/003/005, RSK-006 mới | RSK-006 chưa có owner/trigger/điểm; không có quy trình issue. Thêm register ngắn (Appendix C). Due 2026-11-02 | PO | Non-blocking |
| 19 | Change Control Management | Pass | SDP §5 Change control (hook `.claude/baselined.txt` tồn tại; CR → PO duyệt → tag `*-v2`) | `change-requests.md` chưa tồn tại: tạo khi có CR đầu tiên | PO | Non-blocking |
| 20 | Software Configuration Management (SCM) | Pass | SDP §6.1 nhánh, tag baseline, submodule `6996dae` | — | Tech Lead | Non-blocking |
| 21 | Quality Assurance & Verification/Validation | Pass | SDP §6.2 cổng lint/pytest/golden RC-2/review RC-5/TEST_CASES (RC-2, RC-5 có ở PRD §5) | — | PO | Non-blocking |
| 22 | Documentation & Maintenance Plan | Pass | SDP §6.3 | — | PO | Non-blocking |

**Tổng:** Pass 16 · Partial 6 · Fail 0 · N/A 0.

## 2. Kiểm tra task card (TaskBreakdown §7.2 3.4) và truy vết

| Kiểm tra | Kết quả | Evidence |
|---|---|---|
| 20 trường front-matter bắt buộc | Pass | Script kiểm `task_id … status` trên 12 card: không thiếu trường nào |
| 14 mục Markdown theo thứ tự | Pass | Mỗi card có 14 heading `##` (vd. TASK-007 §1..§14) |
| FR-001..020 đều có task | Pass | `requirement_links` phủ đủ 20 FR (FR-020 → TASK-007; FR-018 → TASK-010; FR-019 → TASK-008; FR-003 → TASK-003; FR-011 → TASK-008; FR-012/016 → TASK-004) |
| NFR | Pass | NFR-001/002/003/006/007/010 có task; NFR-004/005/008/009 ghi Inspection ở chặng Test (WBS §5) |
| `design_links` trỏ phần tử thật | Partial | CMP-01..09, ADR-001..004, BRU-001..003, blueprint §2–§7, §6.1–6.7, SAD §3.2/§3.3 đều tồn tại. TASK-011 `SRC-006 D3` là quyết định nguồn (intake), không phải phần tử thiết kế; TASK-012 trỏ tệp checklist kit |
| Phụ thuộc / đường găng | Pass | WBS §3: 001→002→005→006→007→008 (3,75 h) dài hơn nhánh 003→004 (3,0 h); đường găng đúng |

## 3. Vi phạm self-check / anti-pattern của prompt

| ID | Vi phạm | Nguồn | Action | Owner | Gate |
|---|---|---|---|---|---|
| P-1 | SDP thiếu nhiều mục bắt buộc §7.3: front matter đầy đủ, §1 Introduction, §2.6 Assumptions, §2.8 Risk tier, §8 Acceptance/Transition, §9 Compliance/Exceptions, §10 Approvals, Appendix A–H | DevPlan prompt §6 ô 1, §7.3 4.2–4.3 | Hoặc bổ sung các mục (ngắn), hoặc ghi rõ việc rút gọn là tailoring được PO duyệt ở SDP §2. Due 2026-11-02 | PO | Non-blocking |
| P-2 | SDP §7 tự tuyên bố "đã đối chiếu 22 mục" nhưng không có Appendix D có status/evidence | DevPlan prompt §6 ("never report a gate as met without evidence") | Trỏ sang audit này thay cho tự đánh giá, hoặc thêm Appendix D | PO | Non-blocking |
| P-3 | Không có `tasks/INDEX.md` | TaskBreakdown prompt §7.6 Step 5.5 | Tạo INDEX.md (ID, tiêu đề, wave, status) | PO | Non-blocking |
| P-4 | Assumption/open item không có owner + due date (vd. RSK-006, ước lượng) | DevPlan prompt §6 ô 3 | Gộp vào Appendix E | PO | Non-blocking |
| P-5 | `design_links` của TASK-011, TASK-012 không phải phần tử thiết kế | TaskBreakdown §7.2 3.4 | TASK-011 trỏ thêm blueprint §6.0/DEP-002 (bộ văn bản mẫu); TASK-012 có thể ghi `N/A (review task)` | PO | Non-blocking |

## 4. Blocking items

Không có.

## 5. Kết luận

**Gate ready** (0 Fail). Có 6 Partial và 5 vi phạm prompt, đều Non-blocking; nên xử lý P-1 (cấu trúc SDP / Approvals) trước khi gắn tag `plan-v1`. Auditor không phê duyệt; PO quyết định tại cổng.


## Quyết định tại cổng (2026-11-02)

PO duyệt có điều kiện; điều kiện đạt (0 Fail, 0 Blocking). Đã sửa thêm P-1 (tailoring, SDP §7), P-3 (tasks/INDEX.md), P-4 (RSK-006 có owner, trigger, mức). Baseline `plan-v1`.
