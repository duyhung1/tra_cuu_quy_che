# CLAUDE.md — Tra cứu quy chế

Capstone Agentic SDLC. Công ty giả lập **Sao Mai**; PO và người duyệt mọi cổng: **Phùng Duy Hùng**.

## Nguồn sự thật
- Artifact theo chặng trong `docs/01-intake` … `docs/07-verification` (bố cục `sdlc-kit/AI_SDLC-SOP.md` §5). Phiên sau chỉ đọc file, không dựa vào chat.
- Prompt và checklist: submodule `sdlc-kit/` (kit commit `6996dae`). Tham số đã điền cho từng chặng: `prompts/0X-*.md`.
- Truy vết: `docs/03-analysis/traceability.md` (BR → FR → US) và `docs/07-verification/RTM.md` (US/AC → TC → evidence).

## Luật cứng
- Agent soạn và tự audit; **chỉ PO duyệt**, gắn tag baseline (`intake-v1`, `requirements-v1`, …). Agent không tự baseline, không tự kết luận GO.
- Mỗi chặng: Generate → Audit (sub-agent `checklist-auditor`, không sửa artifact) → Fix → PO duyệt. Tối đa 3 vòng.
- Không bịa người, ngày, số liệu: thiếu thì ghi `OQ-xxx` / `ASM-xxx` có owner và hạn.
- Không sửa tài liệu đã baseline; muốn đổi thì tạo change request và PO duyệt. Hook `.claude/hooks/protect_baseline.py` chặn sửa các đường dẫn trong `.claude/baselined.txt`.
- Chỉ dữ liệu giả lập; không commit `.env`, khóa API; không log nội dung câu hỏi, câu trả lời, văn bản.
- Bằng chứng là log, output lệnh, ảnh trong `docs/07-verification/evidence/<run-id>/`; lời agent nói "đã xong" không phải bằng chứng.
- Commit theo Conventional Commits, kèm ID: `docs(requirements): … (BR-001..014)`, `feat(qa): … (TASK-xxx, US-xxx)`.

## Cách chạy một chặng
Dùng skill `sdlc-stage` (`.claude/skills/sdlc-stage/SKILL.md`).
