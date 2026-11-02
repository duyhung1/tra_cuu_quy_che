---
task_id: TASK-006
wbs_element_id: WBS-31
wbs_element_number: "3.1"
wbs_element_name: "Truy xuất"
title: "BM25 trên đơn vị Khoản của văn bản Sẵn sàng"
type: "feature"
slice: "vertical"
priority: "P0"
milestone: "MS-2"
wave: "W2"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "0.5"
estimate_confidence: "Medium"
depends_on: ["TASK-005 (FS)"]
blocks: ["TASK-007"]
requirement_links: ["FR-005", "FR-007", "NFR-001"]
design_links: ["CMP-05", "blueprint §6.4", "ADR-003"]
deliverable: "DEL-3"
risk: "RSK-002"
status: "ready"
---

# TASK-006 — BM25 trên đơn vị Khoản của văn bản Sẵn sàng

## 1. Objective
Câu hỏi về nghỉ phép xếp Điều 7 Nội quy lên đầu.

## 2. Context
Hiện thực CMP-05, blueprint §6.4, ADR-003 cho FR-005, FR-007, NFR-001 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** app/adapters/bm25.py; tests/unit/test_bm25.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `app/adapters/bm25.py` (planned)
- `tests/unit/test_bm25.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- Câu hỏi về nghỉ phép xếp Điều 7 Nội quy lên đầu
- Văn bản không ở trạng thái ready không được trả về (US-002-AC4)

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/unit/test_bm25.py`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-006, FR-005)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-005 (FS). Mở khóa: TASK-007.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
