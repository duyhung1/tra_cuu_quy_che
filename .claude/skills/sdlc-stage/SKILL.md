---
name: sdlc-stage
description: Run one SDLC stage of this project end to end (Generate → Audit → Fix → PO gate) using the kit prompt and checklist. Use when the user asks to do/redo a stage such as intake, BRD, PRD, SAD, plan, build, test or report.
---

# Chạy một chặng SDLC

| Chặng | Prompt (`sdlc-kit/…`) | Checklist | Đầu ra | Tag sau khi duyệt |
|---|---|---|---|---|
| 0 Intake | `requirements/Intake_Intent_Prompt.md` | SOP §5.1 exit criteria | `docs/01-intake/` | `intake-v1` |
| 1 Requirements | `analysis/BRD_Prompt_IEEE_standard.md` | `analysis/BRD_IEEE_29148_Checklist.xlsx` | `docs/02-requirements/BRD.md` | `requirements-v1` |
| 2 Analysis | `analysis/PRD_Prompt_IEEE_standard.md` | `analysis/PRD_IEEE_29148_Checklist.xlsx` | `docs/03-analysis/` | `analysis-v1` |
| 3 Design | `design/SAD_Prompt_IEEE_standard.md`, `design/bluePrint_design_prompt.md`, diagram prompts | `design/SAD_IEEE_1016_Checklist.xlsx` + UML checklists | `docs/04-design/` | `design-v1` |
| 4 Planning | `development/DevPlan_ISO_24748_5_Prompt.md`, `development/TaskBreakdown_ISO_21511_Prompt.md` | `development/DevPlan_ISO_24748_5_Checklist.xlsx` | `docs/05-development/` | `plan-v1` |
| 5 Build | `development/Implementation_Task_Prompt.md` | `verification/Code_Review_IEEE_1028_Checklist.xlsx` | mã nguồn + PR | `build-v1` |
| 6 Test | `verification/TestPlan_IEEE 829-2008_prompt.md`, `verification/TestCase_RTM_IEEE_829_Prompt.md` | `verification/Test_Plan_IEEE_829_Checklist.xlsx` | `docs/07-verification/` | `verification-v1` |
| 7 Report | `verification/TestReport_IEEE_829_Prompt.md` | IEEE 829 + evidence log | `docs/07-verification/TEST_REPORT.md` | `release-v1` (chỉ khi PO kết luận GO) |

## Các bước
1. **Specify:** kiểm tra đầu vào của chặng trước đã có tag baseline. Điền `prompts/0X-<chặng>.md` (§2.2 Project parameters). Còn placeholder thì dừng lại và hỏi PO.
2. **Generate:** chạy prompt với tệp tham số; ghi đúng đường dẫn đầu ra, kèm document control (owner, ngày, version prompt).
3. **Audit:** giao sub-agent `checklist-auditor` chấm theo checklist, ghi `<artifact>-audit.md`. Agent sinh không tự chấm thay.
4. **Fix:** sửa mọi Fail; mỗi Partial phải có owner và hạn. Audit lại. Tối đa 3 vòng, quá thì báo PO.
5. **Gate:** trình PO: tóm tắt, kết quả audit, câu hỏi mở. Chỉ khi PO duyệt mới ghi xác nhận vào artifact, commit, gắn tag và thêm đường dẫn vào `.claude/baselined.txt`.
