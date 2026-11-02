---
task_id: TASK-007
wbs_element_id: WBS-32
wbs_element_number: "3.2"
wbs_element_name: "Luật hiệu lực"
title: "Resolver: văn bản hiệu lực muộn hơn, văn bản chưa hiệu lực"
type: "feature"
slice: "vertical"
priority: "P0"
milestone: "MS-2"
wave: "W2"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "1.0"
estimate_confidence: "Medium"
depends_on: ["TASK-006 (FS)"]
blocks: ["TASK-008"]
requirement_links: ["FR-009", "FR-010", "FR-020", "US-004", "US-006"]
design_links: ["CMP-06", "blueprint §6.5", "BRU-001", "BRU-003"]
deliverable: "DEL-3"
risk: "RSK-001"
status: "done"
---

# TASK-007 — Resolver: văn bản hiệu lực muộn hơn, văn bản chưa hiệu lực

## 1. Objective
Khoản 1 Điều 5 Quy chế 08/2025 bị thay bởi Quyết định 02/2026 (đã hiệu lực) → primary là đơn vị của Quyết định, superseded có Khoản cũ (US-004-AC1, AC2).

## 2. Context
Hiện thực CMP-06, blueprint §6.5, BRU-001, BRU-003 cho FR-009, FR-010, FR-020, US-004, US-006 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** app/services/resolver.py; tests/unit/test_resolver.py.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `app/services/resolver.py` (planned)
- `tests/unit/test_resolver.py` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- Khoản 1 Điều 5 Quy chế 08/2025 bị thay bởi Quyết định 02/2026 (đã hiệu lực) → primary là đơn vị của Quyết định, superseded có Khoản cũ (US-004-AC1, AC2)
- Khoản 2 Điều 5 không bị thay (chỉ khoản 1)
- Văn bản sửa đổi có ngày hiệu lực > today → giữ đơn vị cũ, upcoming có ngày (US-006-AC1)

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `tests/unit/test_resolver.py`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-007, US-004, US-006)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-006 (FS). Mở khóa: TASK-008.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
