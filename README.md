# Tra cứu quy chế

Capstone khóa Agentic SDLC: tra cứu quy chế nội bộ của một công ty giả lập (Sao Mai). Câu trả lời có căn cứ Điều/Khoản.

Dự án đi theo 8 chặng của bộ prompt và checklist [`sdlc-kit/`](sdlc-kit), là submodule [SDLC-Prompt-Checklist](https://github.com/minhtrantrong/SDLC-Prompt-Checklist). Mỗi chặng cho ra artifact trong `docs/`, được tự audit theo checklist, và chỉ sang chặng sau khi PO duyệt.

| Chặng | Thư mục | Trạng thái |
|---|---|---|
| 0 Intake | [docs/01-intake](docs/01-intake) | Đã duyệt (`intake-v1`) |
| 1 Requirements (BRD) | [docs/02-requirements](docs/02-requirements) | Đã duyệt (`requirements-v1`) |
| 2 Analysis (PRD, User Stories) | [docs/03-analysis](docs/03-analysis) | Đã duyệt (`analysis-v1`) |
| 3 Design (SAD, blueprint, sơ đồ) | [docs/04-design](docs/04-design) | Đã duyệt (`design-v1`) |
| 4 Planning (kế hoạch, tasks) | [docs/05-development](docs/05-development) | Đã duyệt (`plan-v1`) |
| 5 Build | `app/`, `web/`, `tests/` | Đã duyệt (`build-v1`) |
| 6 Test (plan, cases, RTM) | docs/07-verification | Chưa bắt đầu |
| 7 Report (TEST_REPORT) | docs/07-verification | Chưa bắt đầu |

Tham số dùng để chạy từng prompt nằm trong [`prompts/`](prompts).

```bash
git clone --recurse-submodules https://github.com/duyhung1/tra_cuu_quy_che.git
```
