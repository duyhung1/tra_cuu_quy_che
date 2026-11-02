---
task_id: TASK-004
wbs_element_id: WBS-22
wbs_element_number: "2.2"
wbs_element_name: "Xử lý tệp"
title: "Kiểm tra tệp, trích PDF, lọc chỉ dẫn, dịch vụ ingest"
type: "feature"
slice: "vertical"
priority: "P0"
milestone: "MS-2"
wave: "W1"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "1.0"
estimate_confidence: "Medium"
depends_on: ["TASK-003 (FS)", "TASK-005 (SS)"]
blocks: ["TASK-009"]
requirement_links: ["FR-001", "FR-002", "FR-012", "FR-016", "NFR-002", "NFR-010", "US-001", "US-008"]
design_links: ["CMP-03", "SAD §3.2", "blueprint §6.6", "ADR-004"]
deliverable: "DEL-2"
risk: "RSK-002"
status: "done"
---

# TASK-004 — Kiểm tra tệp, trích PDF, lọc chỉ dẫn, dịch vụ ingest

## 1. Objective
Mỗi lỗi not_pdf, file_too_large, too_many_pages, encrypted_pdf, no_text_layer, corrupted, duplicate_name, collection_full trả đúng mã (US-001-AC3..AC6).

## 2. Context
Hiện thực CMP-03, SAD §3.2, blueprint §6.6, ADR-004 cho FR-001, FR-002, FR-012, FR-016, NFR-002, NFR-010, US-001, US-008 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** app/adapters/pdf_pymupdf.py; app/services/ingest.py; tests/unit/test_ingest.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `app/adapters/pdf_pymupdf.py` (planned)
- `app/services/ingest.py` (planned)
- `tests/unit/test_ingest.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- Mỗi lỗi not_pdf, file_too_large, too_many_pages, encrypted_pdf, no_text_layer, corrupted, duplicate_name, collection_full trả đúng mã (US-001-AC3..AC6)
- Câu chỉ dẫn bị loại, `units_filtered` tăng (US-008-AC1)
- Một tệp lỗi không ảnh hưởng tệp khác (US-001-AC3)

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/unit/test_ingest.py`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-004, US-001, US-008)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-003 (FS), TASK-005 (SS). Mở khóa: TASK-009.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
