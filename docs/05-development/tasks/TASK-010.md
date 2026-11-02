---
task_id: TASK-010
wbs_element_id: WBS-41
wbs_element_number: "4.1"
wbs_element_name: "Giao diện"
title: "Web UI tĩnh: Tra cứu và Văn bản"
type: "feature"
slice: "vertical"
priority: "P0"
milestone: "MS-2"
wave: "W2"
owner_role: "Developer (AI agent), reviewer: PO"
estimate_hours: "1.0"
estimate_confidence: "Medium"
depends_on: ["TASK-009 (FS)"]
blocks: ["TASK-012"]
requirement_links: ["FR-001", "FR-004", "FR-006", "FR-008", "FR-013", "FR-015", "FR-018", "NFR-007", "US-001", "US-002", "US-003", "US-009", "US-010"]
design_links: ["CMP-01", "blueprint §7"]
deliverable: "DEL-4"
risk: "RSK-002"
status: "ready"
---

# TASK-010 — Web UI tĩnh: Tra cứu và Văn bản

## 1. Objective
Chọn 11 tệp bị chặn trước khi gửi (US-001-AC2).

## 2. Context
Hiện thực CMP-01, blueprint §7 cho FR-001, FR-004, FR-006, FR-008, FR-013, FR-015, FR-018, NFR-007, US-001, US-002, US-003, US-009, US-010 [Source: docs/04-design/SAD.md, docs/04-design/blueprint.md, docs/03-analysis/PRD.md].

## 3. Scope
- **In:** web/index.html; web/app.js; web/app.css; web/vi.json.
- **Out:** mọi thứ ngoài các tệp trên; không thêm tính năng ngoài PRD.

## 4. Inputs
`docs/04-design/blueprint.md`, `docs/04-design/SAD.md`, `docs/03-analysis/USER_STORIES.md`, `CLAUDE.md`.

## 5. Files and components touched
- `web/index.html` (planned)
- `web/app.js` (planned)
- `web/app.css` (planned)
- `web/vi.json` (planned)

## 6. Implementation guidance
- Giữ quy tắc phụ thuộc SAD §2.3 (chỉ `app/wiring.py` import adapter).
- Không ghi câu hỏi, câu trả lời, văn bản vào log (NFR-003).
- Thông điệp người dùng chỉ lấy từ `app/domain/errors.py` / `web/vi.json` (NFR-007).

## 7. Acceptance criteria
- Chọn 11 tệp bị chặn trước khi gửi (US-001-AC2)
- Khối Căn cứ hiện [n] Điều — tên · số hiệu · hiệu lực · trang (US-003-AC2)
- Bận → giữ câu hỏi, nút Hỏi lại (US-010-AC1)
- Chưa có văn bản → khóa ô hỏi (US-009-AC1)
- Câu trả lời chèn bằng textContent

## 8. Verification
```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
```
Kỳ vọng: 0 lỗi lint, mọi test xanh. Test của task: `docs/07-verification: TC-UI-* chạy trên trình duyệt`.

## 9. Definition of Done
- [ ] Test của task được viết và xanh
- [ ] `ruff` sạch, toàn bộ `pytest` xanh
- [ ] Commit `feat(...)/test(...): … (TASK-010, US-001, US-002, US-003, US-009, US-010)`
- [ ] `docs/07-verification/RTM.md` cập nhật khi chặng Test tới

## 10. Risks and mitigations
Logic sai làm trích sai căn cứ (RSK-001): test unit với văn bản mẫu thật; golden set đo lại.

## 11. Rollback
`git revert` commit của task; không có migration ngoài lược đồ tạo mới.

## 12. Dependencies and ordering notes
Phụ thuộc: TASK-009 (FS). Mở khóa: TASK-012.

## 13. Execution guardrails
Agent chỉ sửa các tệp ở §5; không sửa tài liệu đã baseline (hook `protect_baseline.py`); tối đa 3 vòng sửa khi test đỏ rồi báo PO; PO duyệt ở cổng Build.

## 14. Open questions
Không có.
