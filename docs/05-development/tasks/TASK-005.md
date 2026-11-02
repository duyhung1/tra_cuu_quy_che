---
task_id: TASK-005
wbs_element_id: WBS-23
wbs_element_number: "2.3"
wbs_element_name: "Lưu trữ"
title: "Store SQLite và usage log"
type: "feature"
slice: "vertical"
priority: "P0"
milestone: "MS-2"
wave: "W1"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "0.5"
estimate_confidence: "Medium"
depends_on: ["TASK-002 (FS)"]
blocks: ["TASK-004", "TASK-006"]
requirement_links: ["FR-004", "FR-005", "FR-014", "FR-017", "NFR-003", "US-007"]
design_links: ["CMP-04", "CMP-09", "blueprint §4", "ADR-002"]
deliverable: "DEL-2"
risk: "RSK-002"
status: "done"
---

# TASK-005 — Store SQLite và usage log

## 1. Objective
Lược đồ đúng blueprint §4; mỗi tệp một transaction.

## 2. Context
Hiện thực CMP-04, CMP-09, blueprint §4, ADR-002 cho FR-004, FR-005, FR-014, FR-017, NFR-003, US-007 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** app/adapters/sqlite_store.py; tests/integration/test_store.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `app/adapters/sqlite_store.py` (planned)
- `tests/integration/test_store.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- Lược đồ đúng blueprint §4; mỗi tệp một transaction
- ask_log chỉ có at, latency_ms, status, cited_count (US-007-AC1)

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/integration/test_store.py`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-005, US-007)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-002 (FS). Mở khóa: TASK-004, TASK-006.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
