---
task_id: TASK-002
wbs_element_id: WBS-12
wbs_element_number: "1.2"
wbs_element_name: "Kiểu miền và lỗi"
title: "Kiểu miền, bảng mã lỗi tiếng Việt, chuẩn hóa và tách từ"
type: "feature"
slice: "vertical"
priority: "P0"
milestone: "MS-2"
wave: "W1"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "0.5"
estimate_confidence: "Medium"
depends_on: ["TASK-001 (FS)"]
blocks: ["TASK-003", "TASK-005"]
requirement_links: ["FR-002", "FR-006", "NFR-007"]
design_links: ["blueprint §3", "blueprint §5", "blueprint §6.4"]
deliverable: "DEL-1"
risk: "RSK-002"
status: "done"
---

# TASK-002 — Kiểu miền, bảng mã lỗi tiếng Việt, chuẩn hóa và tách từ

## 1. Objective
13 mã lỗi của blueprint §5 có thông điệp tiếng Việt và HTTP status.

## 2. Context
Hiện thực blueprint §3, blueprint §5, blueprint §6.4 cho FR-002, FR-006, NFR-007 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** app/domain/types.py; app/domain/errors.py; app/domain/text.py; tests/unit/test_text.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `app/domain/types.py` (planned)
- `app/domain/errors.py` (planned)
- `app/domain/text.py` (planned)
- `tests/unit/test_text.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- 13 mã lỗi của blueprint §5 có thông điệp tiếng Việt và HTTP status
- `tokenize` giữ dấu, NFC, lowercase, bỏ stop-word, sinh bigram

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/unit/test_text.py`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-002, FR-002)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-001 (FS). Mở khóa: TASK-003, TASK-005.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
