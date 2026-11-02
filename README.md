# Tra cứu quy chế (MVP)

Ứng dụng web giúp cán bộ, nhân viên tra cứu **quy chế, nội quy và văn bản pháp quy**. Người dùng tải các văn bản PDF lên rồi hỏi bằng tiếng Việt. AI (Claude) chỉ trả lời dựa trên các văn bản đã tải lên và **ghi rõ căn cứ**: Điều nào, của văn bản nào (số hiệu, ngày hiệu lực), ở trang nào. Khi hai văn bản quy định khác nhau về cùng một việc, văn bản có **hiệu lực muộn hơn** được áp dụng.

MVP có 2 tính năng:

- **F1 — Xử lý văn bản**: nhận diện số hiệu, tên, ngày hiệu lực; tách văn bản theo Chương → Điều → Khoản.
- **F2 — Tra cứu có căn cứ**: hỏi đáp kèm trích dẫn `[n]`.

MVP không có đăng nhập; truy cập được giới hạn theo IP / VPN ở tầng mạng. Thiết kế luồng chi tiết nằm ở [docs/Thiet_ke_luong.md](docs/Thiet_ke_luong.md).

## Kiến trúc

```
Trình duyệt ─► web (React SPA, Nginx) ─► api (FastAPI) ─► PostgreSQL 16 + pgvector
                                            │   └──────► Anthropic API (Claude)
                                            └──► S3 (tệp PDF)
worker (Python) ─► S3 → PyMuPDF → metadata → chunk theo Điều → TEI (bge-m3) → pgvector
```

| Thư mục | Nội dung |
|---|---|
| `backend/app/platform/` | Cấu hình, DB, lỗi problem+json, log JSON, lưu trữ S3 |
| `backend/app/modules/documents/` | Tải lên, hàng đợi xử lý, trích xuất PDF, **nhận diện cấu trúc Điều/Khoản và metadata**, chunker |
| `backend/app/modules/qa/` | Truy xuất vector, prompt, adapter Claude, use case tra cứu, **trích dẫn căn cứ** |
| `backend/app/worker/` | Tiến trình xử lý văn bản |
| `backend/tests/` | Test đơn vị, test tích hợp (Testcontainers), golden set (`eval/`), PDF mẫu giả lập |
| `frontend/src/` | SPA: trang Văn bản và Tra cứu |
| `infra/` | Compose production, script deploy / rollback, hướng dẫn dựng AWS |
| `docs/` | Thiết kế luồng, danh sách task |

## Chạy local

Yêu cầu: Docker, Python ≥ 3.12, Node 20+.

```bash
cp .env.example .env          # điền ANTHROPIC_API_KEY để tra cứu được
make venv                     # virtualenv backend + dependencies
make dev                      # postgres, s3 (S3Mock), tei, api, worker, web
make seed                     # tải 3 văn bản mẫu (Công ty Sao Mai, giả lập)
```

- Web: http://localhost:5173 · API docs: http://localhost:8000/api/v1/docs
- Lần chạy đầu, TEI tải model `BAAI/bge-m3` (~2,3 GB).
- Trên Windows, virtualenv nằm ở `backend/.venv/Scripts/` thay vì `.venv/bin/`. Chạy các lệnh `make` trong Git Bash hoặc WSL, hoặc gọi trực tiếp `backend/.venv/Scripts/pytest`.

Thử các câu hỏi sau với bộ văn bản mẫu:

- "Phụ cấp lưu trú khi đi công tác hiện nay là bao nhiêu?" → 450.000 đồng/ngày theo Điều 1 Quyết định 02/2026, thay thế Điều 5 của Quy chế 08/2025.
- "Làm 6 năm được nghỉ phép bao nhiêu ngày?" → 13 ngày (Điều 7 Nội quy lao động).

## Kiểm tra chất lượng

```bash
make lint        # ruff + mypy, eslint + tsc
make test        # pytest (unit + tích hợp, cần Docker) và vitest
make eval BASE_URL=http://localhost:8000   # golden set; chấm cột correct rồi `make eval-score`
```

## Deploy

Xem [infra/README.md](infra/README.md). Chạy `make eval` trước mỗi lần deploy.
