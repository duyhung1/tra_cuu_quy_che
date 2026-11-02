# Software Development Plan — Tra cứu quy chế

| Mục | Giá trị |
|---|---|
| Document ID | TCQC-SDP |
| Version | 1.0 |
| Status | Baselined — `plan-v1` (PO, 2026-11-02) |
| Owner / Approver | Phùng Duy Hùng (PO, kiêm Tech Lead) |
| Author | AI agent (Claude Code) |
| Date | 2026-11-02 |
| Prompt | `sdlc-kit/development/DevPlan_ISO_24748_5_Prompt.md` v2.0; tham số `prompts/05-development.md` |
| Đầu vào | BRD (`requirements-v1`), PRD/US (`analysis-v1`), SAD/blueprint/ADR (`design-v1`) |
| Đi kèm | [WBS.md](WBS.md), [tasks/](tasks) |

## 1. Project overview & context

| Mục | Nội dung |
|---|---|
| Purpose & scope | Hiện thực FR-001..020, NFR-001..010 của PRD v1.0 (phạm vi ở PRD §1.3) |
| Business drivers | BO-001..004 (BRD §4.4) |
| System context | SAD §2.1: một tiến trình nội bộ, không kết nối ra ngoài (SRC-006 D4) |
| Standards | ISO/IEC/IEEE 24748-5 (kế hoạch), ISO 21511 (WBS), IEEE 1028 (review), IEEE 829 (test), `sdlc-kit/AI_SDLC-SOP.md` |

## 2. Lifecycle & process

- **Mô hình:** Incremental (PRD DELIVERY_MODEL). Ba wave trong một ngày:
  - **W1:** khung, miền, xử lý văn bản, dữ liệu mẫu;
  - **W2:** tra cứu, API, giao diện;
  - **W3:** review.
- **Quy trình mỗi task:**
  1. Đọc task card và blueprint.
  2. Viết test trước hoặc cùng lúc với code.
  3. Chạy `ruff` và `pytest`.
  4. Commit `feat|test(...): … (TASK-xxx, US-xxx)`.
  5. Tối đa 3 vòng sửa; quá thì báo PO.
- **Tailoring:**
  - một người kiêm PO, Tech Lead và reviewer;
  - AI agent là developer;
  - không có CI từ xa trong ngày; cổng chất lượng chạy cục bộ (§6.2) và lưu output làm bằng chứng.
- **Deliverables:**

| ID | Deliverable | Task |
|---|---|---|
| DEL-1 | Khung + miền | TASK-001, 002 |
| DEL-2 | Kho văn bản | TASK-003, 004, 005 |
| DEL-3 | Tra cứu | TASK-006, 007, 008, 009 |
| DEL-4 | Giao diện | TASK-010 |
| DEL-5 | Dữ liệu kiểm thử | TASK-011 |
| DEL-6 | Biên bản review | TASK-012 |

## 3. Organization & governance

| Vai trò | Người | Trách nhiệm |
|---|---|---|
| PO / Tech Lead / Reviewer | Phùng Duy Hùng | Duyệt mọi cổng, review code (IEEE 1028), GO/NO-GO |
| Developer | AI agent (Claude Code) | Code, test, tài liệu theo task card |
| Auditor | Sub-agent `checklist-auditor` | Chấm artifact theo checklist, không sửa, không duyệt |

- **Governance:** cổng sau mỗi chặng (SRC-006 D8). Agent không tự baseline (CON-07).
- **Stakeholder management:** STK-01..05 (BRD §4.6). Giảng viên nhận repo khi nghiệm thu.

## 4. Resources & estimation

- **Ước lượng:** theo kinh nghiệm cho từng task (WBS §2), tổng 8,75 giờ công agent, độ tin cậy Medium. Đơn vị là giờ thực hiện của agent kèm thời gian PO duyệt.
- **Nhân lực:** 1 PO, 1 AI agent.
- **Hạ tầng và công cụ:** máy Windows của PO, Python 3.12+, venv `.venv`, FastAPI, PyMuPDF, pytest, ruff, git + GitHub (`duyhung1/tra_cuu_quy_che`). Không cần Docker hay dịch vụ ngoài.
- **Ngân sách:** không công bố (dự án học tập, BRD §4.2). Chi phí dịch vụ ngoài: 0 (SRC-006 D4).

## 5. Monitoring & control

| Milestone | Nội dung | Đích |
|---|---|---|
| MS-1 | `plan-v1` | 2026-11-02 |
| MS-2 | W1 + W2 xong, test xanh | 2026-11-02 |
| MS-3 | Review IEEE 1028 xong, `build-v1` | 2026-11-02 |
| MS-4 | `verification-v1`, TEST_REPORT có GO/NO-GO | 2026-11-02 |

- **Theo dõi tiến độ:** trạng thái task trong front-matter của task card và commit có mã task; README hiển thị trạng thái từng chặng.
- **Rủi ro** (sổ rủi ro chính ở BRD §4.10; mọi rủi ro do PO làm owner, xem lại tại mỗi cổng): RSK-001, RSK-002, RSK-003, RSK-005 (BRD §4.10, PRD §6). Rủi ro kế hoạch:
  - **RSK-006** (owner: PO; trigger: 23:30 mà chưa xong W2; mức: High): vượt thời gian trong ngày → ưu tiên P0; P1 (FR-010, FR-013, FR-017) có thể chuyển sang sau. Mọi phần chưa làm phải ghi trong TEST_REPORT.
- **Change control:** tài liệu đã baseline bị hook chặn sửa (`.claude/baselined.txt`). Muốn thay đổi phải ghi change request trong `docs/05-development/change-requests.md`, PO duyệt, rồi gắn tag `*-v2`.

## 6. Technical support processes

### 6.1 SCM

- Một repo git; nhánh `restart` sẽ thay `main` khi PO duyệt push.
- Baseline bằng tag: `intake-v1`, `requirements-v1`, `analysis-v1`, `design-v1`, `plan-v1`, `build-v1`, `verification-v1`.
- `sdlc-kit` là submodule, khóa ở commit `6996dae`.
- Không commit `.env`, `.venv`, `data/`.

### 6.2 QA, verification & validation

| Cổng | Lệnh / hoạt động | Ngưỡng |
|---|---|---|
| Lint | `.venv/Scripts/python -m ruff check app tests` | 0 lỗi |
| Unit + integration | `.venv/Scripts/python -m pytest -q` | 100 % xanh |
| Golden set | `.venv/Scripts/python tests/golden/run_golden.py` | RC-2 (PRD §5.1) |
| Review | `docs/07-verification/code-review.md` (IEEE 1028) | 0 Major mở |
| Test hệ thống | `docs/07-verification/TEST_CASES.md` | 100 % P0 Pass, có bằng chứng |

### 6.3 Documentation & maintenance

README (cách chạy), CLAUDE.md (luật cho agent), docs theo chặng. Bảo trì sau capstone: OQ-001 (đo baseline), RSK-004/005 (thay adapter trả lời thì đo lại).

## 7. Tailoring

SDP rút gọn so với cấu trúc §7.3 của prompt: một người, một ngày, dữ liệu giả lập (CON-01, CON-02). Các mục bị gộp:

- Introduction, Assumptions → §1, BRD §4.10;
- Risk tier → Medium (intake);
- Acceptance/Transition → PRD §5.1, TEST_REPORT;
- Compliance → không có (CON-02);
- Approvals → tag baseline;
- Appendices A–H → WBS, task card, audit.

PO chấp nhận việc rút gọn này khi duyệt cổng.

**Theo dõi:** KPI là số task `done` / 12 và số test xanh, báo tại mỗi cổng.

## 8. Self-check

Đã đối chiếu 22 mục của `DevPlan_ISO_24748_5_Checklist.xlsx`. Điểm chính thức: [sdp-audit.md](sdp-audit.md).
