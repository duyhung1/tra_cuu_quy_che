# Test Plan (IEEE 829-2008) — Tra cứu quy chế

| Mục | Giá trị |
|---|---|
| 1.0 Test plan identifier | TCQC-TP-001, version 0.1 |
| Status | In review |
| Owner / Approver | Phùng Duy Hùng (PO) |
| Author | AI agent (Claude Code) |
| Date | 2026-11-02 |
| Prompt | `sdlc-kit/verification/TestPlan_IEEE 829-2008_prompt.md` v2.0 |
| Đầu vào | PRD/US v1.0 (`analysis-v1`), SAD/blueprint (`design-v1`), SDP/WBS (`plan-v1`), CR-001, `code-review.md` |

## 2.0 Introduction

Kế hoạch kiểm thử cho bản phát hành đầu tiên của TCQC. Mục tiêu: chứng minh bằng bằng chứng mở được rằng các tiêu chí phát hành RC-1..RC-6 (PRD §5.1) đạt hay không, làm cơ sở cho GO/NO-GO. Tham chiếu: BRD, PRD, USER_STORIES, SAD, blueprint, SDP.

## 3.0 Test items

Repo `duyhung1/tra_cuu_quy_che`, nhánh `restart`, commit ghi trong `run-id`. Gồm:
- `app/` (CMP-02..09);
- `web/` (CMP-01);
- dữ liệu mẫu `tests/fixtures/pdfs/` (DEP-002);
- golden set `tests/golden/golden.json` (DEP-003).

## 4.0 Features to be tested

| Feature | US | FR / NFR | Mức |
|---|---|---|---|
| Đưa văn bản vào, lỗi theo tệp | US-001 | FR-001, FR-002, FR-016, NFR-010 | Unit, integration, UI |
| Danh sách văn bản, metadata | US-002 | FR-003, FR-004, FR-005, FR-018 | Unit, integration, UI |
| Trả lời có căn cứ | US-003 | FR-006, FR-007, FR-008, FR-019 | Unit, golden, UI |
| Văn bản hiệu lực muộn hơn | US-004 | FR-009, FR-020 | Unit, golden |
| Không tìm thấy | US-005 | FR-011 | Unit, golden |
| Sắp có hiệu lực | US-006 | FR-010 | Unit, golden |
| Số liệu không nội dung | US-007 | FR-014, FR-017, NFR-003 | Integration, golden |
| Chống chỉ dẫn trong văn bản | US-008 | FR-012 | Unit, golden |
| Chưa có văn bản | US-009 | FR-013 | Integration, UI |
| Hệ thống bận | US-010 | FR-015 | Integration |
| Hiệu năng | — | NFR-001, NFR-002, NFR-006 | Golden, integration |
| Ngôn ngữ, phạm vi truy cập, sẵn sàng, mã hóa, phân quyền | — | NFR-004, NFR-005, NFR-007, NFR-008, NFR-009 | Inspection, diễn tập |

## 5.0 Features not to be tested

- Mọi mục out of scope của PRD §1.3 (đăng nhập, OCR, DOCX, di động…).
- MET-001 và MET-005 với người dùng thật (deferred, OQ-001).
- Chất lượng câu trả lời với mô hình ngôn ngữ bên ngoài (SRC-006 D4, D5; RSK-005).

## 6.0 Approach

| Mức | Công cụ | Lệnh |
|---|---|---|
| Lint | ruff | `.venv/Scripts/python -m ruff check app tests` |
| Unit + integration | pytest, FastAPI TestClient, SQLite tạm | `.venv/Scripts/python -m pytest -q` |
| Hệ thống (golden set) | `tests/golden/run_golden.py`, chấm tự động theo `expect_*`, PO duyệt kết quả | `.venv/Scripts/python tests/golden/run_golden.py --out <evidence>` |
| UI | Trình duyệt tích hợp của Claude Code (agent điều khiển), chụp màn hình | Chạy `uvicorn app.main:app` với `TCQC_DB` tạm |
| Inspection | Đọc cấu hình và code, đối chiếu NFR | Ghi vào `evidence/<run-id>/inspection.md` |
| Diễn tập phục hồi | Xóa CSDL, đưa lại 3 văn bản, đo thời gian | Ghi vào `evidence/<run-id>/recovery.txt` |

- Ngày tham chiếu cố định `TCQC_TODAY=2026-11-02`, để kết quả về hiệu lực tái lập được.
- `run-id = <yyyymmdd-hhmm>-<commit7>-local-win`.

## 7.0 Item pass/fail criteria

| Mã | Tiêu chí |
|---|---|
| RC-1 | 100 % test pytest xanh, ruff 0 lỗi |
| RC-2 | MET-002 ≥ 80 %, MET-003 = 100 %, MET-004 ≥ 90 %, MET-007 ≥ 80 %, p90 ≤ 30 s, 0 lộ nội dung |
| RC-3 | 100 % test case P0 PASS, có bằng chứng |
| RC-4 | NFR-003: 0 lần câu hỏi xuất hiện trong log hoặc tệp CSDL |
| RC-5 | `code-review.md` không còn Major mở |
| RC-6 | PO ký GO |

## 8.0 Suspension and resumption

- **Tạm dừng:** ứng dụng không khởi động được, hoặc dữ liệu mẫu sai.
- **Tiếp tục:** sau khi sửa và chạy lại toàn bộ từ đầu với `run-id` mới.

## 9.0 Test deliverables

- `TEST_PLAN.md`, `TEST_CASES.md`, `RTM.md`, `TEST_REPORT.md`.
- `evidence/<run-id>/`: `pytest.txt`, `ruff.txt`, `golden-results.json`, `app.log`, `leak-check.txt`, `ui-*.png`, `inspection.md`, `recovery.txt`.

## 10.0 Testing tasks

1. Chạy RC-1.
2. Chạy golden set (RC-2, RC-4).
3. Chạy UI.
4. Inspection và diễn tập.
5. Điền RTM.
6. Viết TEST_REPORT.
7. PO quyết định GO/NO-GO.

## 11.0 Environment

Windows 10 Pro 19045, Python 3.13 (venv), FastAPI, PyMuPDF; trình duyệt Chromium tích hợp. Mạng: localhost.

## 12.0 Responsibilities, 13.0 Staffing

| Vai trò | Người |
|---|---|
| Thực thi | AI agent |
| Duyệt kết quả golden set, ký GO/NO-GO | PO Phùng Duy Hùng |

## 14.0 Schedule

Cùng ngày 2026-11-02, sau cổng Build (SDP MS-4).

## 15.0 Risks and contingencies

| Rủi ro | Xử lý |
|---|---|
| RSK-002 hết giờ | Giữ bằng chứng, cắt bề rộng: P1 UI có thể SKIP có lý do |
| RSK-005 golden set đo trên thành phần trả lời nội bộ | Ghi rõ trong TEST_REPORT |

## 16.0 Approvals

PO Phùng Duy Hùng, tại cổng Test.
