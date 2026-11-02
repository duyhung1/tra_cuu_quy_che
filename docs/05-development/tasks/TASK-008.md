---
task_id: TASK-008
wbs_element_id: WBS-33
wbs_element_number: "3.3"
wbs_element_name: "Dựng câu trả lời"
title: "RuleBasedAnswerer: câu trả lời có [n], NOT_FOUND, sources"
type: "feature"
slice: "vertical"
priority: "P0"
milestone: "MS-2"
wave: "W2"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "0.75"
estimate_confidence: "Medium"
depends_on: ["TASK-007 (FS)"]
blocks: ["TASK-009"]
requirement_links: ["FR-007", "FR-008", "FR-011", "FR-019", "US-003", "US-005"]
design_links: ["CMP-07", "blueprint §6.7", "ADR-001"]
deliverable: "DEL-3"
risk: "RSK-001"
status: "ready"
---

# TASK-008 — RuleBasedAnswerer: câu trả lời có [n], NOT_FOUND, sources

## 1. Objective
Câu dương tính có [1] và source đủ năm thành phần (US-003-AC2).

## 2. Context
Hiện thực CMP-07, blueprint §6.7, ADR-001 cho FR-007, FR-008, FR-011, FR-019, US-003, US-005 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** app/adapters/rule_answerer.py; tests/unit/test_answerer.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `app/adapters/rule_answerer.py` (planned)
- `tests/unit/test_answerer.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- Câu dương tính có [1] và source đủ năm thành phần (US-003-AC2)
- Dưới ngưỡng → đúng câu NOT_FOUND, sources rỗng (US-005-AC1)
- superseded / upcoming sinh câu "thay thế" / "sắp có hiệu lực" có [n]

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/unit/test_answerer.py`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-008, US-003, US-005)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-007 (FS). Mở khóa: TASK-009.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
