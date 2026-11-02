# AGENTS.md — hướng dẫn cho AI agent và developer

Repo của MVP **"Tra cứu quy chế"**: tải quy chế, nội quy, văn bản pháp quy (PDF) lên, hỏi bằng tiếng Việt. AI (Claude) chỉ trả lời dựa trên các văn bản đó, có trích dẫn căn cứ theo Điều. Phạm vi: **F1 — Xử lý văn bản** (metadata + tách Điều/Khoản) và **F2 — Tra cứu có căn cứ**.

## Nguồn sự thật

| Câu hỏi | Xem ở |
|---|---|
| Bài toán, luồng F1/F2, dữ liệu, task | `docs/Thiet_ke_luong.md` |
| Cách chạy | `README.md` |

## Cấu trúc

```
backend/app/platform/            config, DB, lỗi problem+json, log JSON, lưu trữ S3
backend/app/modules/documents/   tải lên, hàng đợi trong PostgreSQL, trích xuất PDF, cấu trúc Điều/Khoản + metadata, chunker
backend/app/modules/qa/          port, truy xuất vector, prompt, adapter Claude, use case tra cứu, trích dẫn
backend/app/worker/              tiến trình xử lý tài liệu
backend/app/migrations/          Alembic
backend/tests/                   unit/ · integration/ (Testcontainers) · eval/ (golden set) · fixtures/ · fakes/
frontend/src/                    app/ (shell, router) · features/{documents,ask} · shared/{api,ui,i18n}
infra/                           compose production, deploy.sh, rollback.sh, hướng dẫn AWS
```

## Lệnh

```bash
make venv          # virtualenv backend (Python 3.12)
make dev           # stack local: postgres, s3 (S3Mock), tei, api, worker x2, web
make seed          # tải 3 PDF mẫu lên stack đang chạy
make lint          # ruff + mypy · eslint + tsc
make test          # pytest (cần Docker cho Testcontainers) · vitest
make eval BASE_URL=http://localhost:8000   # golden set; chấm cột correct rồi `make eval-score`
```

Chạy một test backend: `cd backend && .venv/bin/pytest tests/unit/test_chunker.py -q`.

## Quy tắc bắt buộc

- **Kiến trúc:** use case trong `modules/*/application/` chỉ phụ thuộc vào port (`modules/qa/ports.py`, `platform/storage.py`); **không** import FastAPI hay SDK `anthropic` / boto3 ở đó. Đổi nhà cung cấp AI chỉ được phép bằng cách thêm adapter mới.
- **Không log nội dung** câu hỏi, câu trả lời hay văn bản tài liệu; `qa_log` chỉ lưu số liệu.
- **Lỗi API** luôn là `AppError(code)` có trong `platform/errors.py::ERRORS`. Thêm mã mới thì thêm cả thông điệp tiếng Việt trong `frontend/src/shared/i18n/vi.json`.
- **Chuỗi giao diện** chỉ nằm trong `vi.json`, không viết cứng trong TSX.
- **Câu trả lời của AI** phải render qua `features/ask/markdown.ts` (marked + DOMPurify).
- **Trích dẫn:** câu trả lời dẫn trích đoạn bằng `[n]`; `qa/application/citations.py` lọc số không tồn tại và dựng `sources`. Đổi định dạng `[n]` thì sửa cả prompt, `citations.py` và test.
- **Nhận diện cấu trúc:** mẫu Chương / Điều / Khoản / số hiệu / ngày hiệu lực nằm trong `ingestion/legal_structure.py`; thêm mẫu mới phải có test trong `tests/unit/test_legal_structure.py`.
- **Prompt:** mọi thay đổi `modules/qa/prompts.py` phải chạy lại `make eval` và ghi điểm trước / sau vào mô tả PR.
- **CSDL:** thay đổi lược đồ bằng revision Alembic mới; không sửa `0001_init.py` sau khi đã merge.
- **Bí mật:** không commit `.env`, khóa API hay dữ liệu thật của khách hàng; fixture PDF chỉ là dữ liệu giả lập.
- **Không có đăng nhập** trong MVP: bảo vệ dựa vào giới hạn IP / VPN của ALB (`infra/README.md`). Không mở ALB ra `0.0.0.0/0`.

## Git

- Mỗi commit thuộc **một task**, tiêu đề bắt đầu bằng mã task: `T-013: Add ingestion pipeline and worker`. Sửa lỗi của task cũ cũng dùng mã task đó.
- Trước khi commit: `make lint` và `make test` phải xanh.
- Cập nhật bảng task trong `docs/Thiet_ke_luong.md` khi thêm task hoặc file chính.

## Môi trường local — lưu ý

- Image TEI CPU chỉ có bản amd64; trên Mac Apple Silicon chạy giả lập, lần đầu tải model khoảng 2,3 GB.
- Docker Desktop cần ≥ 8 GB RAM; compose đã giảm `--max-batch-tokens` của TEI xuống 2048 để không bị hết bộ nhớ.
- Không có `ANTHROPIC_API_KEY` thì `/api/v1/ask` trả **503 `ai_unavailable`**; các phần còn lại vẫn chạy.
- S3 local là Adobe S3Mock (MinIO đã ngừng phát hành image công khai); dữ liệu lưu trong volume `s3data`.
