# ADR-001: Câu trả lời do RuleBasedAnswerer trong tiến trình tạo ra, sau port Answerer

| Mục | Giá trị |
|---|---|
| Trạng thái | Đề xuất (chờ PO duyệt cùng SAD) |
| Ngày | 2026-11-02 |
| Liên quan | FR-007, FR-008, FR-011, FR-012, FR-019; BR-004..008; RSK-004, RSK-005 |

## Bối cảnh

PO quyết định không gửi nội dung ra ngoài và không có API key (SRC-006 D4, D5). FR-007..011 cần câu trả lời có căn cứ, đúng hiệu lực, từ chối khi không có.

## Quyết định

Answerer là một port. Adapter của bản phát hành này là `RuleBasedAnswerer`: trích nguyên văn Khoản tốt nhất, thêm chú thích thay thế / sắp hiệu lực, trả NOT_FOUND khi dưới ngưỡng (blueprint §6.7).

## Lựa chọn đã xét

| Phương án | Lý do không chọn |
|---|---|
| Gọi Claude API | Không có key; trái SRC-006 D4 |
| Mô hình ngôn ngữ chạy cục bộ | Tải mô hình nhiều GB, chậm trên CPU, không kịp CON-01 |
| Chỉ trả danh sách đoạn văn, không câu trả lời | Không đạt FR-009/FR-020 (nêu văn bản bị thay) |

## Hệ quả

Câu trả lời không tóm tắt hay diễn giải; chất lượng phụ thuộc truy xuất (RSK-005). Thay bằng adapter khác chỉ cần cài port `Answerer`, sau đó chạy lại golden set. Không có rủi ro prompt injection kiểu LLM; vẫn giữ bộ lọc §6.6 cho BR-012.
