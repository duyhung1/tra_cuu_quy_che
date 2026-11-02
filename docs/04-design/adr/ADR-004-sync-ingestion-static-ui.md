# ADR-004: Xử lý văn bản đồng bộ trong yêu cầu tải lên; giao diện HTML/JS tĩnh

| Mục | Giá trị |
|---|---|
| Trạng thái | Đã chấp nhận (PO, 2026-11-02, cùng `design-v1`) |
| Ngày | 2026-11-02 |
| Liên quan | NFR-002, FR-001, FR-002, FR-004, FR-018, NFR-007 |

## Bối cảnh

Văn bản ≤ 20 trang phải sẵn sàng ≤ 60 giây (NFR-002); trích văn bản + nhận diện chỉ tốn chưa tới một giây/văn bản. Hạn trong ngày (CON-01).

## Quyết định

API-01 xử lý từng tệp ngay trong yêu cầu, trả trạng thái cuối (`ready`/`failed`). UI là HTML/JS/CSS tĩnh do FastAPI phục vụ, không cần bước build.

## Lựa chọn đã xét

| Phương án | Lý do không chọn |
|---|---|
| Hàng đợi + worker | Thêm tiến trình, trạng thái trung gian, không cần với kho nhỏ |
| SPA React/Vite | Cần build, nhiều phụ thuộc; không cần cho hai màn hình |

## Hệ quả

Tải 10 tệp 300 trang có thể mất lâu trong một yêu cầu; chấp nhận cho capstone. Trạng thái `processing` chỉ thấy trong lúc tải lên (FR-018 vẫn áp dụng khi nhiều người cùng tải).
