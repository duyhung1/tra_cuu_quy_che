# ADR-003: Truy xuất BM25 trên đơn vị Khoản

| Mục | Giá trị |
|---|---|
| Trạng thái | Đã chấp nhận (PO, 2026-11-02, cùng `design-v1`) |
| Ngày | 2026-11-02 |
| Liên quan | FR-005, FR-007, FR-008, NFR-001, NFR-006; BR-005 |

## Bối cảnh

Căn cứ phải đúng Điều/Khoản (BR-005). Không có dịch vụ embedding (SRC-006 D4). Kho nhỏ.

## Quyết định

Đơn vị = một Khoản (hoặc cả Điều nếu không có Khoản), tiền tố tiêu đề Điều. BM25 unigram + bigram, chỉ mục dựng trong bộ nhớ khi kho thay đổi (blueprint §6.4).

## Lựa chọn đã xét

| Phương án | Lý do không chọn |
|---|---|
| Embedding (bge-m3) + vector | Tải mô hình 2,3 GB, cần dịch vụ riêng, không kịp |
| Chunk theo trang | Căn cứ không chỉ ra được Khoản; trộn nhiều Điều |
| Tìm chuỗi đơn giản (LIKE) | Không xếp hạng được |

## Hệ quả

Không hiểu từ đồng nghĩa (hạn chế đã biết, blueprint §9). Bù lại: nhanh, tất định, giải thích được (matched_terms).
