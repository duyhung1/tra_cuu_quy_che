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
| 6 Test (plan, cases, RTM) | [docs/07-verification](docs/07-verification) | Đã duyệt (`verification-v1`) |
| 7 Report (TEST_REPORT) | [TEST_REPORT.md](docs/07-verification/TEST_REPORT.md) | **GO with conditions** (`release-v1`) |

Tham số dùng để chạy từng prompt nằm trong [`prompts/`](prompts). Thay đổi sau baseline nằm trong [`docs/change-requests/`](docs/change-requests).

## Truy vết nhanh (demo)

BR → FR → US → TC → bằng chứng:

1. [BRD §4.11](docs/02-requirements/BRD.md)
2. [traceability.md](docs/03-analysis/traceability.md)
3. [RTM.md](docs/07-verification/RTM.md)
4. [evidence/](docs/07-verification/evidence)

Ví dụ: BR-006 → FR-009 → US-004 → TC-011 → `evidence/…/golden-results.json` (G-09) và `ui-answer.jpg`.

## Chạy

Yêu cầu: Python ≥ 3.12. Không cần Docker, không cần API key (ADR-001).

```bash
python -m venv .venv
.venv/Scripts/python -m pip install fastapi uvicorn pymupdf python-multipart pytest httpx ruff
.venv/Scripts/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Mở http://127.0.0.1:8000, vào trang **Văn bản** và chọn các PDF trong `tests/fixtures/pdfs/sample/`.

```bash
.venv/Scripts/python -m ruff check app tests
.venv/Scripts/python -m pytest -q
.venv/Scripts/python tests/golden/run_golden.py --out docs/07-verification/evidence/<run-id>
```

Trên Linux/macOS dùng `.venv/bin/` thay cho `.venv/Scripts/`.

```bash
git clone --recurse-submodules https://github.com/duyhung1/tra_cuu_quy_che.git
```
