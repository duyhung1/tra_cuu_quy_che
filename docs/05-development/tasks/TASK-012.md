---
task_id: TASK-012
wbs_element_id: WBS-61
wbs_element_number: "6.1"
wbs_element_name: "Review code"
title: "Review code theo IEEE 1028 và sửa lỗi Major"
type: "documentation"
slice: "horizontal"
priority: "P0"
milestone: "MS-3"
wave: "W3"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "0.5"
estimate_confidence: "Medium"
depends_on: ["TASK-010 (FS)"]
blocks: []
requirement_links: ["RC-5"]
design_links: ["verification/Code_Review_IEEE_1028_Checklist.xlsx"]
deliverable: "DEL-6"
risk: "RSK-002"
status: "done"
---

# TASK-012 — Review code theo IEEE 1028 và sửa lỗi Major

## 1. Objective
Mọi dòng checklist IEEE 1028 có Status + Evidence; 0 lỗi Major còn mở.

## 2. Context
Hiện thực verification/Code_Review_IEEE_1028_Checklist.xlsx cho RC-5 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** docs/07-verification/code-review.md.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `docs/07-verification/code-review.md` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- Mọi dòng checklist IEEE 1028 có Status + Evidence; 0 lỗi Major còn mở

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `docs/07-verification/code-review.md`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-012, RC-5)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-010 (FS). Mở khóa: không.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
