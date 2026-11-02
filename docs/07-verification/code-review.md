# Code Review — TASK-001..011 (IEEE 1028)

## 1. Kiểm soát tài liệu

| Mục | Giá trị |
|---|---|
| Dự án | Tra cứu quy chế |
| Loại review | Technical review (IEEE 1028), reviewer độc lập, read-only (AI) |
| Nhánh / commit được review | `restart` @ `a4e19d4` (phê duyệt chỉ áp dụng cho commit này) |
| Phạm vi commit | `plan-v1..a4e19d4` — 11 commit, TASK-001..TASK-011 (`git diff plan-v1..HEAD -- app web tests`: 49 file, +2086) |
| Baseline thiết kế | `docs/04-design/SAD.md`, `blueprint.md`, `adr/` (tag `design-v1`) |
| Yêu cầu | `docs/03-analysis/PRD.md`, task card `docs/05-development/tasks/`, `docs/change-requests/CR-001.md` |
| Checklist | `sdlc-kit/verification/Code_Review_IEEE_1028_Checklist.xlsx` (19 mục) |
| Ngày | 2026-11-02 |
| Người phê duyệt | Phùng Duy Hùng (PO) — bản review này **không** thay thế phê duyệt của người |
| Giới hạn | Review có giới hạn thời gian (~7 phút): đọc kỹ `resolver.py`, `legal_parser.py`, `ask.py`, `logging_setup.py`, `main.py`, `wiring.py`, các sink DOM trong `web/app.js`; các file còn lại chỉ đọc lướt. |

## 2. Checklist

Status: Pass / Fail / Partial / N/A. Gate: Build.

| # | Category | Checklist Item | Status | Evidence | Notes | Owner | Gate |
|---|---|---|---|---|---|---|---|
| 1 | 1. Preparation & Metadata | Review Objective | Pass | Mục 1 | Tìm lỗi + kiểm tra tuân thủ blueprint §6, NFR-003, layering | Reviewer | Build |
| 2 | 1. Preparation & Metadata | Entry Criteria | Pass | Diff, task card, SAD/blueprint, PRD, CR-001 có sẵn; pytest/ruff chạy được | | Reviewer | Build |
| 3 | 2. Architecture & Design | Design Conformance | Partial | `resolver.py` khớp §6.5 bước 1–7; `legal_parser.py` lệch §6.0/§6.3 | CR-001 thêm `min_coverage` và khoản cùng Điều, chưa duyệt; xem CR-R-03..05 | Developer | Build |
| 4 | 2. Architecture & Design | Modularity | Pass | Chỉ `app/wiring.py` import `app.adapters` (grep); `tests/unit/test_import_rules.py` | Service chỉ phụ thuộc `app.ports` | — | Build |
| 5 | 3. Logic & Functionality | Requirements Coverage | Partial | `ask.py:48-57` (khoản cùng Điều), `resolver.py:74` (coverage) | Tính năng ngoài baseline thuộc CR-001; hợp lệ khi PO duyệt | PO | Build |
| 6 | 3. Logic & Functionality | Boundary Conditions | Partial | `ask.py:61` (1..2000), `resolver.py:36,94` (MAX_CHAIN) | Xem CR-R-04, CR-R-06 | Developer | Build |
| 7 | 3. Logic & Functionality | Variable Initialization | Pass | `ask.py:66`, `resolver.py:73` | Không thấy biến dùng trước khi gán | — | Build |
| 8 | 4. Error Handling & Logging | Exception Handling | Partial | `ask.py:67-81` | Timeout/exception → `error` + 503 `ai_unavailable` đúng SAD §3.3; nhưng luồng hết giờ vẫn chạy và state retriever không an toàn đa luồng (CR-R-01, CR-R-02) | Developer | Build |
| 9 | 4. Error Handling & Logging | Meaningful Messages | Partial | `main.py:29-31` | AppError trả `code`+`message` tiếng Việt; lỗi validate body (422 mặc định FastAPI) không theo bảng lỗi (CR-R-07) | Developer | Build |
| 10 | 5. Security | Input Validation | Pass | `web/app.js:1,11` chỉ dùng `textContent`; không có `innerHTML`/`outerHTML`/`insertAdjacentHTML` (grep) | Không thấy XSS; giới hạn kích thước upload `main.py:42` | — | Build |
| 11 | 5. Security | Authentication/Authorization | N/A | PRD/SAD: MVP không có đăng nhập | | — | Build |
| 12 | 6. Performance & Efficiency | Resource Management | Partial | `ask.py:18` pool 16 luồng toàn cục | Tác vụ hết giờ không bị hủy, chiếm luồng (CR-R-02) | Developer | Build |
| 13 | 6. Performance & Efficiency | Algorithmic Efficiency | Partial | `resolver.py:46-68` | `targets()`/`amenders()` O(A·U) mỗi lần gọi, gọi trong vòng lặp; chấp nhận được với quy mô MVP (CR-R-08) | Developer | Build |
| 14 | 7. Maintainability & Readability | Coding Standards | Pass | `ruff check app tests` → All checks passed! | | — | Build |
| 15 | 7. Maintainability & Readability | Naming Conventions | Pass | Tên theo ký hiệu blueprint (`h0`, `base`, `applied`, `superseded`) | | — | Build |
| 16 | 7. Maintainability & Readability | Code Comments | Pass | Docstring dẫn chiếu blueprint §, comment theo bước thuật toán | | — | Build |
| 17 | 8. Testing & Validation | Unit Test Coverage | Partial | `test_resolver.py` có đủ (a)–(f) của §6.5; không có test cho timeout 30 s, ghi ASK_LOG lỗi, hay truy cập đồng thời | CR-R-09 | Developer | Build |
| 18 | 8. Testing & Validation | Test Success | Pass | `43 passed, 1 warning in 11.13s` | | — | Build |
| 19 | 9. Exit Criteria | Action Items Addressed | Fail | Mục 3 | 2 Major còn mở; CR-001 chờ PO | Developer / PO | Build |

Tổng: Pass 9 · Partial 8 · Fail 1 · N/A 1.

## 3. Findings

| ID | Severity | File:line | Mô tả | Đề xuất |
|---|---|---|---|---|
| CR-R-01 | Major | `app/services/ask.py:36-39`, `app/adapters/bm25.py:16-25` | `_refresh()` chạy trong pool đa luồng, không có khóa. `rebuild()` gán lần lượt `units`, `tf`, `len`, `idf` — một request khác đang `search()` có thể đọc trạng thái trộn cũ/mới (vd. `KeyError` ở `self.len[u.id]`) ngay sau khi có tài liệu mới, và hai request có thể rebuild cùng lúc. Lỗi bị nuốt thành 503 `ai_unavailable` giả. | Thêm `threading.Lock` quanh refresh + search, hoặc dựng index mới rồi gán một tham chiếu duy nhất (atomic swap). |
| CR-R-02 | Major | `app/services/ask.py:18,68` | Hết 30 s chỉ bỏ chờ `result()`; tác vụ vẫn chạy trên `_pool` (16 luồng). Các truy vấn chậm tích lũy làm cạn pool, request sau xếp hàng và cũng hết giờ (FR-015, NFR-001). Không có test cho đường timeout. | Ghi nhận giới hạn trong ADR/SAD hoặc giới hạn hàng đợi; thêm test timeout với answerer giả chậm và `timeout_s` nhỏ. |
| CR-R-03 | Minor | `app/services/legal_parser.py:10` | `DOC_NO` khác §6.0 (bắt buộc ký tự cuối là chữ/số). Hợp lý (bỏ dấu `/`, `-` thừa) nhưng không có trong CR-001. | Bổ sung vào CR-001 hoặc cập nhật blueprint. |
| CR-R-04 | Minor | `app/services/legal_parser.py:122,126` | Số hiệu văn bản đích chỉ tìm trong phần thân trước Khoản đầu tiên, không tìm trong các Khoản; §6.3 bước 1 nói "thân Điều". Điều sửa đổi chỉ ghi số hiệu trong Khoản sẽ không tạo liên kết. | Tìm trên toàn bộ văn bản Điều (body + clauses). |
| CR-R-05 | Minor | `app/services/legal_parser.py:107-109` | `K(N)` khóa theo số Điều, không theo `DOC_NO` của câu (§6.3 bước 2); văn bản sửa cùng số Điều của hai văn bản khác nhau sẽ bị trộn. | Khóa theo `(doc_no, article_no)`. |
| CR-R-06 | Minor | `app/services/resolver.py:108-123` | Khi bước 6 đổi `applied` sang văn bản không liên kết, `upcoming` (bước 5) không được tính lại theo `applied` mới. Blueprint không yêu cầu rõ thứ tự này. | Làm rõ trong blueprint hoặc tính lại `upcoming`. |
| CR-R-07 | Minor | `app/main.py:19,64` | Body sai kiểu → 422 mặc định của FastAPI (trả lại `input` của client), không phải mã trong bảng lỗi tiếng Việt. | Thêm handler `RequestValidationError` → `question_invalid`. |
| CR-R-08 | Minor | `app/services/resolver.py:46-68` | Quét toàn bộ `amendments × units` mỗi lần gọi `targets/amenders`. | Lập chỉ mục theo `(doc_number, article_no)` khi cần. |
| CR-R-09 | Minor | `tests/` | Không có test kiểm tra log/ASK_LOG không chứa nội dung (NFR-003) ở mức unit; chỉ có trong `tests/golden/run_golden.py:93`. | Thêm test `caplog` cho `ask`/`ingest`. |
| CR-R-10 | Minor | `app/services/legal_parser.py:51` | Nếu mẫu 1/2 khớp nhưng ngày không hợp lệ, code rơi xuống mẫu "từ ngày ký" — lệch nhẹ quy tắc "mẫu đầu tiên khớp được dùng" (§6.2). | Dừng khi mẫu đã khớp. |

Kiểm tra không phát hiện lỗi:
- **NFR-003:** `JsonFormatter` chỉ xuất `event` + danh sách trường số/ID cố định (`logging_setup.py:6-16`); exception chỉ ghi `exc_type`, không ghi message/traceback. `UsageRecord` chỉ có latency, status, cited_count (`ask.py:77`). Không có đường nào đưa câu hỏi/câu trả lời/văn bản vào log hoặc ask_log.
- **XSS:** `web/app.js` chỉ ghi DOM bằng `textContent`.
- **Layering:** chỉ `app/wiring.py` import `app.adapters`.
- **Resolver vs §6.5:** bước 1–7 và các test bắt buộc (a)–(f) khớp; A3 (văn bản không rõ ngày, `eff = date.min`) không thay thế văn bản khác.

## 4. Đánh giá CR-001

Có căn cứ. (1) `min_coverage` giải quyết trường hợp âm tính FR-011 mà τ không chặn được; (2) đưa khoản cùng Điều vào câu trả lời giúp trả lời đủ; (3) bỏ "trong" khỏi stop-word nằm trong phạm vi tinh chỉnh §6.4 cho phép. Bằng chứng golden set được dẫn chiếu. Đề nghị PO duyệt, kèm thêm CR-R-03 (DOC_NO) vào CR, và ghi giá trị cuối vào TEST_REPORT.

## 5. Bằng chứng test / lint (commit `a4e19d4`)

```
> .venv/Scripts/python -m pytest -q
...........................................                              [100%]
.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
43 passed, 1 warning in 11.13s

> .venv/Scripts/python -m ruff check app tests
All checks passed!
```

## 6. Khuyến nghị cho PO

**Approve with conditions** — 2 Major, 8 Minor.
Điều kiện: (1) sửa CR-R-01 (an toàn đa luồng khi rebuild/search) và có test; (2) xử lý hoặc ghi nhận CR-R-02 và thêm test timeout 30 s; (3) PO quyết định CR-001 tại cổng Build. Các Minor có thể chuyển sang backlog.
