---
task_id: TASK-001
wbs_element_id: WBS-11
wbs_element_number: "1.1"
wbs_element_name: "Khung mã nguồn"
title: "Khung repo: config, wiring, app FastAPI, healthz, import-rule test"
type: "infrastructure"
slice: "horizontal"
priority: "P0"
milestone: "MS-2"
wave: "W1"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "0.5"
estimate_confidence: "Medium"
depends_on: []
blocks: ["TASK-002", "TASK-011"]
requirement_links: ["NFR-007"]
design_links: ["CMP-02", "blueprint §2"]
deliverable: "DEL-1"
risk: "RSK-002"
status: "done"
---

# TASK-001 — Khung repo: config, wiring, app FastAPI, healthz, import-rule test

## 1. Objective
`GET /healthz` trả 200 `{status: ok}`.

## 2. Context
Hiện thực CMP-02, blueprint §2 cho NFR-007 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** pyproject.toml; app/__init__.py; app/config.py; app/wiring.py; app/main.py; app/ports.py; tests/unit/test_import_rules.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `pyproject.toml` (planned)
- `app/__init__.py` (planned)
- `app/config.py` (planned)
- `app/wiring.py` (planned)
- `app/main.py` (planned)
- `app/ports.py` (planned)
- `tests/unit/test_import_rules.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- `GET /healthz` trả 200 `{status: ok}`
- Chỉ `app/wiring.py` import `app.adapters`; `app/domain`, `app/services` không import fastapi/pymupdf/sqlite3

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/unit/test_import_rules.py`, `tests/integration/test_api.py::test_healthz`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-001, NFR-007)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: không. Mở khóa: TASK-002, TASK-011.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
