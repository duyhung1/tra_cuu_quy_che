# Work item WI-001 — Tra cứu quy chế nội bộ có căn cứ Điều/Khoản

| Mục | Giá trị |
|---|---|
| ID | WI-001 |
| Phiên bản | 0.1 |
| Trạng thái | Chờ PO xác nhận intake |
| Owner | Phùng Duy Hùng (PO) |
| Ngày | 2026-11-02 |
| Prompt | `sdlc-kit/requirements/Intake_Intent_Prompt.md` v2.0 |
| Intent | [intent.md](intent.md) |

## Thông tin work item

| Trường | Giá trị |
|---|---|
| Problem / outcome | [intent.md](intent.md) §1–2 |
| Người dùng | Nhân viên, hành chính – nhân sự, pháp chế / kế toán ([stakeholders.md](stakeholders.md)) |
| Ưu tiên | P0: hạn nghiệm thu 2026-11-02 (CON-01) |
| Risk tier | Medium ([intent.md](intent.md) §Risk tier) |
| Người duyệt | Phùng Duy Hùng (PO), ở mọi cổng |

## Tiêu chí chấp nhận của work item

| ID | Tiêu chí | Đo bằng |
|---|---|---|
| WI-AC-01 | Người dùng hỏi bằng tiếng Việt và nhận câu trả lời chỉ dựa trên văn bản đã đưa vào | SM-02, SM-04 |
| WI-AC-02 | Mỗi câu trả lời có căn cứ: Điều/Khoản, tên văn bản, số hiệu, ngày hiệu lực | SM-02 |
| WI-AC-03 | Khi các văn bản khác nhau về cùng một việc, quy định của văn bản có hiệu lực muộn hơn được áp dụng và nêu rõ văn bản bị thay thế | SM-03 |
| WI-AC-04 | Câu hỏi ngoài phạm vi được trả lời "không tìm thấy" | SM-04 |
| WI-AC-05 | Thời gian trả lời đạt SM-01 | SM-01 |
| WI-AC-06 | Đủ 8 chặng SDLC, mỗi chặng qua cổng của PO, có bằng chứng thật | CON-06 |

## Ràng buộc với agent, công cụ và dữ liệu

- Agent được dùng: Claude Code. Agent soạn artifact, code và test; agent **không** duyệt, baseline, merge hay kết luận GO (SOP §3).
- Dữ liệu đưa cho agent và dịch vụ AI: chỉ dữ liệu giả lập (CON-02). Không có bí mật, khóa API hay dữ liệu cá nhân trong repo.
- Mọi thay đổi đi qua commit có mã task; mọi cổng được ghi lại trong lịch sử git (tag baseline).

## Tự kiểm theo SOP §5.1 exit criteria

| # | Hạng mục | Status | Evidence |
|---|---|---|---|
| 1 | Có human owner, tiêu chí chấp nhận và risk tier | Pass | WI-001 §Thông tin, §Tiêu chí chấp nhận; intent.md §Risk tier |
| 2 | Mỗi success measure có baseline, target, cách đo | Pass | intent.md §5: SM-01..05. Baseline chưa có ghi "Chưa có"; baseline ước lượng gắn ASM-001/002 |
| 3 | Out of scope ghi rõ; mọi nguồn có SRC-xxx | Pass | intent.md §6; sources.md SRC-001..004 |
| 4 | Mọi câu hỏi mở có người trả lời và hạn; không câu hỏi chặn phạm vi nào bị bỏ ngỏ | Partial | OQ-002, OQ-004 chặn phạm vi. Owner: PO; hạn: 2026-11-02, trả lời tại cổng này |
| 5 | Không chứa giải pháp, công nghệ, kiến trúc hay ước lượng công sức | Pass | intent.md không nêu công nghệ; "dựa trên văn bản", "căn cứ" là kết quả mong muốn |
| 6 | Requester xác nhận problem và outcome đúng ý | Partial | Chờ PO xác nhận tại cổng. Owner: PO; hạn: 2026-11-02 |

Kết quả: 4 Pass, 2 Partial (cả hai cần PO trả lời tại cổng), 0 Fail.

## Bàn giao (handoff) sang chặng 1 — Requirements

| Trường | Giá trị |
|---|---|
| Trạng thái | Chờ PO xác nhận intake và trả lời OQ-002, OQ-004 |
| Bằng chứng | `docs/01-intake/*`, commit và tag `intake-v1` sau khi duyệt |
| Người nhận | Phùng Duy Hùng (PO), vai trò chủ yêu cầu ở chặng 1 |
| Rủi ro còn mở | RSK-001, RSK-002 |
| Xác nhận của PO | _(điền khi duyệt: tên, ngày, quyết định)_ |
