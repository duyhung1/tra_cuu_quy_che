# ADR-002: Lưu trữ bằng SQLite nhúng

| Mục | Giá trị |
|---|---|
| Trạng thái | Đã chấp nhận (PO, 2026-11-02, cùng `design-v1`) |
| Ngày | 2026-11-02 |
| Liên quan | NFR-005, NFR-006, NFR-010, FR-014 |

## Bối cảnh

Kho ≤ 50 văn bản (NFR-010), một máy, một người làm trong ngày (CON-01), máy PO không cần Docker (DEP-004).

## Quyết định

Dùng `sqlite3` của thư viện chuẩn, tệp `data/tcqc.db`, chế độ WAL, khóa ngoại bật. Lược đồ ở blueprint §4.

## Lựa chọn đã xét

| Phương án | Lý do không chọn |
|---|---|
| PostgreSQL + pgvector | Cần dựng dịch vụ, không cần vector (ADR-003) |
| Lưu JSON trên đĩa | Không có transaction, khó bảo đảm FR-002 (mỗi tệp độc lập) |

## Hệ quả

Ghi tuần tự, đủ cho mức tải capstone; nhiều tiến trình ghi đồng thời không được hỗ trợ. Phục hồi bằng cách đưa lại văn bản (NFR-005).
