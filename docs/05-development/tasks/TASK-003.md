---
task_id: TASK-003
wbs_element_id: WBS-21
wbs_element_number: "2.1"
wbs_element_name: "Nhận diện văn bản"
title: "Nhận diện Chương/Điều/Khoản, số hiệu, tên, ngày hiệu lực, liên kết sửa đổi"
type: "feature"
slice: "vertical"
priority: "P0"
milestone: "MS-2"
wave: "W1"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "1.0"
estimate_confidence: "Medium"
depends_on: ["TASK-002 (FS)"]
blocks: ["TASK-004"]
requirement_links: ["FR-003", "FR-009", "FR-010", "US-002"]
design_links: ["CMP-03", "blueprint §6.1–6.3", "BRU-002"]
deliverable: "DEL-2"
risk: "RSK-001"
status: "ready"
---

# TASK-003 — Nhận diện Chương/Điều/Khoản, số hiệu, tên, ngày hiệu lực, liên kết sửa đổi

## 1. Objective
Mỗi Khoản thành một Unit có article_no, clause_no, page; tham chiếu "theo Điều 5 của" không bị nhận là tiêu đề.

## 2. Context
Hiện thực CMP-03, blueprint §6.1–6.3, BRU-002 cho FR-003, FR-009, FR-010, US-002 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** app/services/legal_parser.py; tests/unit/test_legal_parser.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `app/services/legal_parser.py` (planned)
- `tests/unit/test_legal_parser.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- Mỗi Khoản thành một Unit có article_no, clause_no, page; tham chiếu "theo Điều 5 của" không bị nhận là tiêu đề
- Số hiệu, tên, ngày hiệu lực đúng cho 100 % văn bản mẫu; "hiệu lực kể từ ngày ký" → ngày ký
- "thay thế khoản 1 Điều 5 … số 08/2025/QC-SM" tạo một Amendment đúng đích

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/unit/test_legal_parser.py`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-003, US-002)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-002 (FS). Mở khóa: TASK-004.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
