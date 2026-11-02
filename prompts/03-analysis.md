# Chặng 2 — Analysis (PRD, User Stories): tham số chạy prompt

| Mục | Giá trị |
|---|---|
| Prompt | `sdlc-kit/analysis/PRD_Prompt_IEEE_standard.md` v2.0 (kit commit `6996dae`) |
| Checklist | `sdlc-kit/analysis/PRD_IEEE_29148_Checklist.xlsx` → `docs/03-analysis/prd-audit.md` (sub-agent `checklist-auditor`) |
| Đầu vào | `docs/02-requirements/BRD.md` v1.0 (`requirements-v1`), `docs/01-intake/*` (`intake-v1`) |

```yaml
PRODUCT_OR_INITIATIVE: "Tra cứu quy chế (TCQC)"
TARGET_USER_OR_CUSTOMER: "Nhân viên, hành chính – nhân sự, pháp chế / kế toán của Công ty Sao Mai (giả lập)"
PROBLEM_STATEMENT: "Tra quy định mất ~15 phút/lần, dễ dùng quy định đã bị văn bản sau thay thế (BRD §4.3)"
CORE_SOLUTION: "Hỏi bằng tiếng Việt, nhận câu trả lời chỉ dựa trên văn bản nội bộ, kèm căn cứ Điều/Khoản và áp dụng văn bản hiệu lực muộn hơn"
PRODUCT_PILLARS: "Có căn cứ cho mọi ý; đúng văn bản đang hiệu lực; từ chối khi không có; không lưu nội dung"
DOCUMENT_ID: "TCQC-PRD"
DOCUMENT_VERSION: "0.1"
DOCUMENT_OWNER: "Phùng Duy Hùng, PO"
DOCUMENT_APPROVERS: "Phùng Duy Hùng, PO"
OUTPUT_LANGUAGE: "Vietnamese"
PRD_OUTPUT_PATH: "docs/03-analysis/PRD.md"
USER_STORIES_OUTPUT_PATH: "docs/03-analysis/USER_STORIES.md"
DELIVERY_MODEL: "Incremental"
REGULATORY_CONTEXT: "none"
```
