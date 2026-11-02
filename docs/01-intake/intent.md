# Intent — Tra cứu quy chế nội bộ có căn cứ Điều/Khoản

| Mục | Giá trị |
|---|---|
| ID tài liệu | INT-001 |
| Phiên bản | 1.0 |
| Trạng thái | Đã duyệt — baseline `intake-v1` (PO, 2026-11-02) |
| Owner | Phùng Duy Hùng (PO) |
| Ngày | 2026-11-02 |
| Prompt | `sdlc-kit/requirements/Intake_Intent_Prompt.md` v2.0 |

## 1. Problem

Công ty Sao Mai ban hành quy chế, nội quy và các quyết định sửa đổi dưới dạng văn bản rời [Source: SRC-001]. Khi cần biết một quy định (ví dụ mức công tác phí, số ngày phép), nhân viên phải mở từng văn bản, tìm đúng Điều và tự xác định văn bản nào đang có hiệu lực khi đã có quyết định sửa đổi [Source: SRC-001].

- Mỗi lần tra mất khoảng 15 phút [Source: SRC-002, ASM-001].
- Hành chính – nhân sự nhận khoảng 20 câu hỏi lặp lại mỗi tuần [Source: SRC-002, ASM-002].
- Pháp chế / kế toán cần căn cứ chính xác (Điều, Khoản, văn bản) để làm hồ sơ và giải trình. Trích sai, hoặc trích văn bản đã bị thay thế, dẫn tới chi sai và phải làm lại hồ sơ [Source: SRC-001] [Unverified: chưa có số liệu về tần suất sai].

## 2. Proposed outcome

Người dùng đặt câu hỏi bằng tiếng Việt và nhận ngay câu trả lời gồm:

- chỉ dựa trên văn bản nội bộ đã được đưa vào;
- căn cứ cụ thể: Điều/Khoản, tên văn bản, số hiệu, ngày hiệu lực;
- áp dụng quy định của văn bản có hiệu lực muộn hơn khi các văn bản khác nhau về cùng một việc;
- nói rõ "không tìm thấy" khi văn bản không quy định, thay vì đoán [Source: SRC-001].

## 3. Affected users

| Nhóm | Bị ảnh hưởng thế nào | Số lượng |
|---|---|---|
| Nhân viên | Tra quy định khi đi công tác, nghỉ phép, thanh toán… | OQ-003 |
| Hành chính – nhân sự | Đưa văn bản mới vào; giảm việc trả lời câu hỏi lặp | OQ-003 |
| Pháp chế / kế toán | Cần căn cứ chính xác để lập và kiểm hồ sơ | OQ-003 |

[Source: SRC-001]

## 4. Constraints

| ID | Ràng buộc | Nguồn |
|---|---|---|
| CON-01 | Phải hoàn thành và nghiệm thu trong ngày 2026-11-02 | SRC-003 |
| CON-02 | Chỉ dùng dữ liệu giả lập; không có dữ liệu thật của khách hàng hay dữ liệu cá nhân | SRC-001, SRC-003 |
| CON-03 | Nội dung câu hỏi, câu trả lời và văn bản không được ghi vào log | SRC-001 |
| CON-04 | Giao diện và câu trả lời bằng tiếng Việt | SRC-001 |
| CON-05 | Chỉ dùng trong nội bộ công ty, không công khai ra Internet | SRC-001 |
| CON-06 | Đi đủ 8 chặng SDLC; mỗi chặng có artifact, checklist và cổng duyệt của con người | SRC-003, SRC-004 |
| CON-07 | Chỉ một người (PO) vừa yêu cầu vừa duyệt; AI agent soạn, không được tự duyệt hay tự baseline | SRC-003, SRC-004 §3 |

## 5. Success measures

| ID | Chỉ số | Baseline | Target | Cách đo | Owner |
|---|---|---|---|---|---|
| SM-01 | Thời gian từ lúc đặt câu hỏi đến khi có câu trả lời kèm căn cứ | ~15 phút/lần, tra tay (ASM-001) | p90 ≤ 30 giây (hệ thống); ≤ 2 phút gồm cả thao tác của người dùng | Đo độ trễ trên bộ câu hỏi kiểm thử; bấm giờ 5 câu khi nghiệm thu | PO |
| SM-02 | Tỷ lệ câu hỏi có đáp án trả lời đúng và trích đúng Điều | Chưa có (tra tay, không đo) | ≥ 80 % | Chấm bộ câu hỏi chuẩn (golden set) | PO |
| SM-03 | Câu hỏi có văn bản sửa đổi được trả lời theo văn bản hiệu lực muộn hơn | Chưa có | 100 % số câu xung đột trong bộ kiểm thử | Chấm các câu xung đột trong golden set | PO |
| SM-04 | Câu hỏi ngoài phạm vi văn bản được trả lời "không tìm thấy" | Chưa có | ≥ 90 % | Chấm các câu âm tính trong golden set | PO |
| SM-05 | Câu hỏi lặp gửi hành chính – nhân sự | ~20 câu/tuần (ASM-002) | Giảm 50 % sau 1 tháng dùng thử | Đếm yêu cầu gửi HC-NS trước/sau. Ngoài khung capstone (OQ-001) | PO |

## 6. Out of scope

- Đăng nhập, phân quyền theo vai trò, SSO.
- PDF dạng ảnh scan (OCR).
- Soạn thảo, sửa hay phê duyệt văn bản quy chế.
- Tư vấn pháp lý, văn bản pháp luật nhà nước không được đưa vào hệ thống.
- Lưu lịch sử hỏi đáp trên máy chủ.
- Ứng dụng di động, tích hợp với hệ thống nhân sự hay kế toán.
- Đo SM-05 trên người dùng thật (chuyển sang giai đoạn dùng thử sau capstone).

## 7. Open questions

| ID | Câu hỏi | Người trả lời | Cần trước | Chặn phạm vi? |
|---|---|---|---|---|
| OQ-001 | Đo thực tế baseline thời gian tra cứu và số câu hỏi lặp (thay cho ASM-001/002) | PO | 2026-11-30 | Không |
| OQ-002 | Ai được đưa văn bản vào hệ thống: mọi người dùng nội bộ hay chỉ hành chính – nhân sự? Không có đăng nhập thì không phân biệt được người | PO | 2026-11-02 (trước BRD) | **Đã trả lời 2026-11-02:** mọi người dùng nội bộ; truy cập giới hạn ở mạng nội bộ (CON-05); phân quyền để giai đoạn sau |
| OQ-003 | Số người dùng của từng nhóm | PO | 2026-11-30 | Không |
| OQ-004 | Định dạng văn bản đầu vào: chỉ PDF có lớp văn bản là đủ cho giai đoạn này? | PO | 2026-11-02 (trước BRD) | **Đã trả lời 2026-11-02:** chỉ PDF có lớp văn bản; PDF scan báo lỗi rõ ràng |

### Giả định

| ID | Giả định | Owner | Xác nhận bằng |
|---|---|---|---|
| ASM-001 | Baseline thời gian tra cứu khoảng 15 phút/lần là ước lượng của PO, chưa đo | PO | OQ-001 |
| ASM-002 | Khoảng 20 câu hỏi lặp/tuần gửi HC-NS là ước lượng của PO, chưa đo | PO | OQ-001 |

### Rủi ro

| ID | Rủi ro | Ảnh hưởng | Xử lý |
|---|---|---|---|
| RSK-001 | Câu trả lời trích sai Điều hoặc trích văn bản đã bị thay thế | Chi sai, hồ sơ phải làm lại | Bắt buộc có căn cứ; đo SM-02, SM-03 trước khi GO |
| RSK-002 | Hạn trong ngày làm thiếu bằng chứng ở chặng kiểm thử | Không qua nghiệm thu | Cắt bề rộng, giữ bằng chứng: một luồng chính chạy trọn |

## Risk tier đề xuất

**Medium**, theo `sdlc-kit/AI_SDLC-SOP.md` §5.1. Lý do:

- có logic nghiệp vụ, API và xử lý dữ liệu văn bản nội bộ;
- câu trả lời ảnh hưởng tới quyết định chi tiêu (RSK-001);
- không có xác thực, thanh toán hay dữ liệu cá nhân, nên chưa tới High.

**Kiểm soát kèm theo:** human owner; tiêu chí chấp nhận được ghi lại; test tập trung; review có chú ý bảo mật; mọi CI check phải xanh.

## Phê duyệt cần có

| Cổng | Người duyệt | Ghi chú |
|---|---|---|
| Intake (chặng 0) | Phùng Duy Hùng (PO) | Xác nhận problem và outcome đúng ý |
| Mỗi chặng 1–7 | Phùng Duy Hùng (PO) | Agent soạn và tự audit, PO duyệt; agent không bao giờ là người duyệt |
| Review code (IEEE 1028) | Phùng Duy Hùng (PO), người review khác tác giả (agent) | |
| GO/NO-GO trong TEST_REPORT | Phùng Duy Hùng (PO) | |
