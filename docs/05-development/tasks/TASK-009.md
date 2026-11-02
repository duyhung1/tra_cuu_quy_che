---
task_id: TASK-009
wbs_element_id: WBS-34
wbs_element_number: "3.4"
wbs_element_name: "API và dịch vụ hỏi"
title: "Ask service (timeout 30 s, số liệu) và các route API-01..04"
type: "feature"
slice: "vertical"
priority: "P0"
milestone: "MS-2"
wave: "W2"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "0.75"
estimate_confidence: "Medium"
depends_on: ["TASK-004 (FS)", "TASK-008 (FS)"]
blocks: ["TASK-010"]
requirement_links: ["FR-001", "FR-006", "FR-013", "FR-014", "FR-015", "FR-017", "NFR-001", "NFR-006", "US-001", "US-003", "US-007", "US-009", "US-010"]
design_links: ["CMP-02", "CMP-08", "blueprint §5", "SAD §3.3"]
deliverable: "DEL-3"
risk: "RSK-002"
status: "ready"
---

# TASK-009 — Ask service (timeout 30 s, số liệu) và các route API-01..04

## 1. Objective
11 tệp → 400 too_many_files; câu hỏi rỗng / 2001 ký tự → 422; chưa có văn bản → 409.

## 2. Context
Hiện thực CMP-02, CMP-08, blueprint §5, SAD §3.3 cho FR-001, FR-006, FR-013, FR-014, FR-015, FR-017, NFR-001, NFR-006, US-001, US-003, US-007, US-009, US-010 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** app/services/ask.py; app/main.py; tests/integration/test_api.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `app/services/ask.py` (planned)
- `app/main.py` (planned)
- `tests/integration/test_api.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- 11 tệp → 400 too_many_files; câu hỏi rỗng / 2001 ký tự → 422; chưa có văn bản → 409
- Answerer lỗi → 503 ai_unavailable và ask_log status = error (US-010-AC1, US-007-AC3)
- Lỗi ghi ask_log vẫn trả câu trả lời (US-007-AC4)
- 10 câu đồng thời không lỗi (NFR-006)

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/integration/test_api.py`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-009, US-001, US-003, US-007, US-009, US-010)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-004 (FS), TASK-008 (FS). Mở khóa: TASK-010.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
