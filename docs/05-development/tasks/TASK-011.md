---
task_id: TASK-011
wbs_element_id: WBS-51
wbs_element_number: "5.1"
wbs_element_name: "Dữ liệu mẫu và golden set"
title: "Văn bản mẫu giả lập (DEP-002) và golden set (DEP-003)"
type: "test"
slice: "horizontal"
priority: "P0"
milestone: "MS-2"
wave: "W1"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "0.75"
estimate_confidence: "Medium"
depends_on: ["TASK-001 (FS)"]
blocks: []
requirement_links: ["DEP-002", "DEP-003", "MET-002", "MET-003", "MET-004", "MET-007"]
design_links: ["SRC-006 D3"]
deliverable: "DEL-5"
risk: "RSK-002"
status: "ready"
---

# TASK-011 — Văn bản mẫu giả lập (DEP-002) và golden set (DEP-003)

## 1. Objective
Có cặp xung đột (Quy chế 08/2025 ↔ Quyết định 02/2026), một văn bản chưa hiệu lực, một văn bản chứa chỉ dẫn giả, PDF scan / mật khẩu / hỏng / không phải PDF.

## 2. Context
Hiện thực SRC-006 D3 cho DEP-002, DEP-003, MET-002, MET-003, MET-004, MET-007 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** tests/fixtures/make_pdfs.py; tests/fixtures/pdfs/*.pdf; tests/golden/golden.yaml; tests/golden/run_golden.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `tests/fixtures/make_pdfs.py` (planned)
- `tests/fixtures/pdfs/*.pdf` (planned)
- `tests/golden/golden.yaml` (planned)
- `tests/golden/run_golden.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- Có cặp xung đột (Quy chế 08/2025 ↔ Quyết định 02/2026), một văn bản chưa hiệu lực, một văn bản chứa chỉ dẫn giả, PDF scan / mật khẩu / hỏng / không phải PDF
- Golden set ≥ 10 dương tính (≥ 5 FAQ), ≥ 3 xung đột, ≥ 1 chưa hiệu lực, ≥ 5 âm tính

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/golden/run_golden.py`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-011, DEP-002)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-001 (FS). Mở khóa: không.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
