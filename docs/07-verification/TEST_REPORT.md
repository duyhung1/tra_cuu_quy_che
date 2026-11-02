# Test Summary Report (IEEE 829-2008) — Tra cứu quy chế

| Mục | Giá trị |
|---|---|
| Report ID | TCQC-TSR-001, version 1.0 |
| Status | Chờ PO ký |
| Owner / Approver | Phùng Duy Hùng (PO) |
| Author | AI agent (Claude Code) |
| Date | 2026-11-02 |
| Tested commit | `8ae514b` (nhánh `restart`, sau `build-v1` + bản sửa DEF-001) |
| Environment | Windows 10 Pro 19045, Python 3.13 venv, FastAPI/uvicorn, PyMuPDF, SQLite; trình duyệt Chromium tích hợp; localhost; `TCQC_TODAY=2026-11-02` |
| Run id | `20261102-2306-8ae514b-local-win` — [evidence/](evidence/20261102-2306-8ae514b-local-win/) |
| Prompt | `sdlc-kit/verification/TestReport_IEEE_829_Prompt.md` v2.0 |

## 1. Summary

Ngày 2026-11-02, bản phát hành đầu tiên của TCQC (commit `8ae514b`) được kiểm thử ở bốn mức: unit + integration (46 test), hệ thống (golden set 17 câu), giao diện trên trình duyệt, inspection và diễn tập vận hành.

Kết quả theo [RTM](RTM.md): 30 tiêu chí, gồm 28 PASS, 1 SKIP có lý do, 1 GAP có owner, 0 FAIL. 22/22 test case P0 PASS. Tiêu chí phát hành RC-1..RC-5 đạt. Một lỗi phát hiện trong lúc test (DEF-001) đã được sửa và kiểm lại. Hai lỗi Minor còn mở.

## 2. Scope and environment

- **Test items:** `app/`, `web/`, dữ liệu mẫu `tests/fixtures/pdfs/` (5 văn bản giả lập, 4 tệp lỗi), golden set `tests/golden/golden.json`.
- **Mức đã chạy:**

| Mức | Lệnh / công cụ | Bằng chứng |
|---|---|---|
| Lint | `ruff check app tests` | `ruff.txt` |
| Unit + integration | `pytest -v` | `pytest.txt` |
| Hệ thống | `tests/golden/run_golden.py --out …` | `golden-results.json`, `golden-console.txt`, `app.log` |
| Vận hành | `tests/golden/run_ops_checks.py --out …` | `perf.txt`, `recovery.txt` |
| UI | uvicorn 127.0.0.1:8765 + trình duyệt tích hợp | `ui-*.jpg`, `ui-answer.txt`, `ui-documents.txt`, `ui-upload-response.txt`, `ui-app.log` |
| Inspection | đọc code, cấu hình | `inspection.md`, `leak-check.txt` |

- **Loại trừ:** các mục out of scope của PRD §1.3; mô hình ngôn ngữ bên ngoài (SRC-006 D4, D5).

## 3. Variances

| Variance | Lý do | Bản ghi |
|---|---|---|
| Chạy lại toàn bộ với run-id mới | Lần chạy `…-2305-84e30a3…` dừng ở TC-028 vì DEF-001; bằng chứng lần đó đã bỏ và chạy lại trên `8ae514b` | DEF-001, commit `8ae514b` |
| Thêm 3 test so với `build-v1` | 2 test cho review CR-R-01/02, 1 test hồi quy cho DEF-001 | `code-review.md`, `pytest.txt` |
| US-002-AC3 SKIP | Xử lý đồng bộ (ADR-004, OQ-008 đã được PO chấp nhận), nên không có trạng thái "Đang xử lý" kéo dài để quan sát | RTM |
| Upload trên UI qua API | Trình duyệt tự động không chọn được tệp từ ổ đĩa. Văn bản được đưa vào bằng `curl` lên server đang chạy; việc chặn 11 tệp được kiểm trên UI bằng lời gọi `upload()` | `ui-upload-response.txt`, `ui-too-many.jpg` |

## 4. Coverage and results

**Theo mức:**
- pytest: **46 passed**, 0 failed (`pytest.txt`);
- ruff: **All checks passed** (`ruff.txt`);
- golden: **17/17 PASS** (`golden-console.txt`).

**Số đo so với ngưỡng (PRD §5.1, BRD §4.4):**

| Metric / NFR | Ngưỡng | Đo được | Kết quả |
|---|---|---|---|
| MET-002 câu dương tính đúng + đúng Điều | ≥ 80 % (≥ 10 câu) | 12/12 = 100 % | PASS |
| MET-003 câu xung đột | 100 % (≥ 3 câu) | 3/3 | PASS |
| Văn bản chưa hiệu lực (AC-013, AC-015) | đúng (≥ 1 câu) | 1/1 | PASS |
| MET-004 câu âm tính | ≥ 90 % (≥ 5 câu) | 5/5 = 100 % | PASS |
| MET-007 câu FAQ của HC-NS | ≥ 80 % (≥ 5 câu) | 8/8 = 100 % | PASS |
| MET-006 / NFR-001 p90 độ trễ | ≤ 30 000 ms | 18,2 ms | PASS |
| NFR-002 văn bản 20 trang | ≤ 60 s | 0,13 s | PASS |
| NFR-003 lộ nội dung | 0 | 0 (17 câu golden + 2 câu UI, log và CSDL) | PASS |
| NFR-005 phục hồi | ≤ 1 ngày làm việc | 0,18 s cho 5 văn bản | PASS |
| NFR-006 đồng thời | 10 câu không lỗi | 10/10 (và 20 câu + 4 upload xen kẽ) | PASS |

**Tham số trả lời đã dùng:** τ = 2.0, min_coverage = 0.5 (CR-001), stop-word theo `app/domain/text.py`. Không tinh chỉnh thêm sau khi chạy golden set.

**Tiêu chí phát hành:**

| RC | Kết quả |
|---|---|
| RC-1 | Đạt |
| RC-2 | Đạt |
| RC-3 | Đạt (22/22 P0) |
| RC-4 | Đạt |
| RC-5 | Đạt (`code-review.md`: 2 Major đã sửa, PO duyệt cổng Build) |
| RC-6 | Chờ PO ký |

## 5. What was not tested

| Hạng mục | Lý do | Rủi ro còn lại |
|---|---|---|
| MET-001 với người dùng thật (GAP) | Không có người dùng thật trong ngày | Thấp: hệ thống trả lời trong mili-giây; thời gian thao tác của người dùng chưa đo. Owner PO, hạn 2026-11-30 |
| MET-005 (câu hỏi lặp gửi HC-NS) | Deferred theo BRD | Lợi ích kinh doanh chưa được chứng minh |
| Chất lượng với văn bản thật và câu hỏi đa dạng | Golden set nhỏ (17 câu) trên 5 văn bản giả lập do chính dự án soạn | **RSK-005 / hạn chế ADR-003:** BM25 không hiểu từ đồng nghĩa. Câu hỏi diễn đạt khác văn bản có thể bị trả lời "không tìm thấy". Cần mở rộng golden set trên văn bản thật trước khi dùng rộng |
| Mô hình ngôn ngữ bên ngoài | SRC-006 D4, D5 | Khi thay adapter phải chạy lại golden set (RSK-005) |
| Trình duyệt khác Chromium; màn hình nhỏ | Hết thời gian | Thấp |

## 6. Defects and risks

| ID | Mức | Mô tả | Yêu cầu | Trạng thái |
|---|---|---|---|---|
| DEF-001 | Major | SQLite connection không được đóng, khóa tệp CSDL trên Windows (TC-028) | NFR-005 | **Đã sửa** `8ae514b`, test hồi quy `test_store_releases_the_database_file` |
| DEF-002 | Minor | Nút chọn tệp gốc của trình duyệt hiện chữ tiếng Anh "Choose Files / No file chosen" | NFR-007 | Mở; sửa bằng nút tùy chỉnh. Owner PO, backlog |
| DEF-003 | Minor | Tệp bị từ chối trước khi mở PDF (không phải PDF, trùng tên, quá lớn, kho đầy) chỉ báo trong kết quả tải lên, không lưu vào danh sách | FR-004 | Mở; backlog |
| CR-R-03..10 | Minor | 8 Minor của code review | — | Backlog (`code-review.md`) |

**Rủi ro còn lại:** RSK-005 (độ phủ của golden set). RSK-001 được giảm nhờ MET-002/MET-003 đạt 100 % trên golden set, nhưng chỉ trong phạm vi dữ liệu giả lập.

## 7. Evaluation and sign-off

**Đối chiếu GO_CRITERIA** (PRD §5.1 RC-1..RC-6): RC-1..RC-5 đạt; không còn lỗi Major mở; 2 Minor không ảnh hưởng tiêu chí P0.

**Khuyến nghị của agent:** **GO with conditions** cho bản dùng thử nội bộ trên dữ liệu giả lập. Điều kiện:
1. Mở rộng golden set lên văn bản thật và câu hỏi thật của HC-NS trước khi dùng với dữ liệu thật (RSK-005).
2. Đo MET-001 và MET-005 khi dùng thử (OQ-001, hạn 2026-11-30).
3. Xử lý DEF-002, DEF-003 trong backlog.

Agent không được kết luận GO (CON-07); quyết định thuộc PO.

| Vai trò | Tên | Quyết định | Ngày |
|---|---|---|---|
| PO / Approver | Phùng Duy Hùng | _(chờ)_ | |
