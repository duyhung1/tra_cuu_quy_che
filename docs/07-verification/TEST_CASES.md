# Test Cases — Tra cứu quy chế

| Mục | Giá trị |
|---|---|
| ID | TCQC-TC, version 1.0 |
| Owner | Phùng Duy Hùng (PO) |
| Tested commit / environment | ghi trong `RTM.md` (run-id) |
| Date | 2026-11-02 |
| Prompt | `sdlc-kit/verification/TestCase_RTM_IEEE_829_Prompt.md` v2.0 |

**Chung cho mọi case:**
- **Precondition:** `TCQC_TODAY=2026-11-02`; CSDL tạm mới; 5 văn bản mẫu trong `tests/fixtures/pdfs/sample/` (DEP-002) đã được đưa vào, trừ khi ghi khác.
- **Evidence method:** "pytest" nghĩa là dòng PASS của test đó trong `pytest.txt`; "golden" nghĩa là dòng của câu đó trong `golden-results.json`.

| ID | Title | Traces to | P | Preconditions | Steps | Test data | Expected result | Evidence | Type |
|---|---|---|---|---|---|---|---|---|---|
| TC-001 | 3 văn bản hợp lệ chuyển Sẵn sàng | US-001-AC1, AC-001, FR-001 | P0 | Kho trống | 1. Đưa 3 PDF mẫu vào một lần | 3 tệp đầu của `sample/` | 3 × status `ready` | pytest `test_three_valid_documents_become_ready` | Functional |
| TC-002 | Chặn 11 tệp | US-001-AC2, FR-001 | P0 | — | 1. Gửi 11 tệp | 11 tệp `%PDF-` | 400 `too_many_files`, "Mỗi lần chỉ tải tối đa 10 tệp" | pytest `test_eleven_files_is_400`, `test_eleven_files_rejected_as_a_batch`; UI `ui-too-many.png` | Boundary |
| TC-003 | Mỗi tệp lỗi một lý do, tệp hợp lệ vẫn được nhận | US-001-AC3, AC-002, FR-002 | P0 | Kho trống | 1. Gửi 1 tệp hợp lệ + 4 tệp `bad/` | scan, mật khẩu, hỏng, không phải PDF | ready; no_text_layer; encrypted_pdf; corrupted; not_pdf | pytest `test_bad_files_get_one_reason_each…` | Negative |
| TC-004 | Trùng tên, > 20 MB, > 300 trang | US-001-AC4, AC5, FR-002 | P0 | Đã có `a.pdf` | 1. Gửi lại a.pdf + 20 MB + 301 trang | — | duplicate_name; file_too_large; too_many_pages | pytest `test_duplicate_too_large_too_many_pages` | Boundary |
| TC-005 | Kho đầy | US-001-AC6, FR-016 | P0 | max_documents = 2 | 1. Gửi 3 tệp | — | tệp 3: collection_full | pytest `test_collection_full` | Boundary |
| TC-006 | Danh sách có số hiệu, ngày hiệu lực; "kể từ ngày ký" | US-002-AC1, AC2, AC-003, FR-003, FR-004 | P0 | Đã đưa mẫu | 1. GET /api/documents | — | 15/2025/NQ-SM hiệu lực 2025-03-10, tên "NỘI QUY LAO ĐỘNG"; counts ready = 5 | pytest `test_no_documents_then_upload_then_list`; UI `ui-documents.png` | Functional |
| TC-007 | Cấu trúc Điều/Khoản, tham chiếu không phải tiêu đề | FR-003, ASM-004 | P0 | — | 1. parse() văn bản mẫu | QC trong test | units (5,1), (5,2), (9,0); chương đúng | pytest `test_units_per_clause_with_heading_and_chapter`, `test_metadata_*` | Functional |
| TC-008 | Câu trả lời có [n] và căn cứ đủ thành phần | US-003-AC2, AC-005, FR-007, FR-008, FR-019 | P0 | Đã đưa mẫu | 1. Hỏi mức chi tiếp khách | G-04 | 2.000.000; [1] = Điều 8, 08/2025/QC-SM, trang 2, tên, hiệu lực 2025-01-01 | pytest `test_positive_answer_has_reference_and_full_source`; UI `ui-answer.png` | Functional |
| TC-009 | Câu hỏi không hợp lệ | US-003-AC3, FR-006 | P0 | Đã đưa mẫu | 1. Gửi "", "   ", 2001 ký tự | — | 422 question_invalid | pytest `test_invalid_question_is_422` ×3 | Boundary |
| TC-010 | Golden set câu dương tính và FAQ | US-003-AC4, AC-004, AC-016, MET-002, MET-007 | P0 | Golden set | 1. Chạy run_golden.py | G-01..G-12 | MET-002 ≥ 80 %, MET-007 ≥ 80 % | golden summary | Functional |
| TC-011 | Áp dụng văn bản hiệu lực muộn hơn, nêu văn bản bị thay | US-004-AC1, AC2, AC-006, AC-007, FR-009, FR-020 | P0 | Đã đưa mẫu | 1. Hỏi phụ cấp lưu trú hiện nay | G-09 | [1] = 02/2026/QĐ-SM Điều 1; có 450.000, "thay thế", 08/2025/QC-SM, 300.000 | pytest `test_conflict_names_replaced_document_and_old_value`; golden G-09 | Functional |
| TC-012 | Tất cả câu xung đột đúng | US-004-AC3, MET-003 | P0 | Golden set | 1. Chạy run_golden.py | G-09..G-11 | 3/3 | golden summary | Functional |
| TC-013 | Khoản không bị thay vẫn dùng văn bản cũ | FR-009, BRU-001 | P0 | Đã đưa mẫu | 1. Hỏi phụ cấp đi trong ngày | G-07 | 150.000, [1] = 08/2025/QC-SM Điều 5 | golden G-07; pytest `test_b_other_clause_not_superseded` | Functional |
| TC-014 | Luật hiệu lực (a)–(f) | FR-009, FR-010, FR-020, blueprint §6.5 | P0 | — | 1. Chạy test resolver | Unit dựng sẵn | 6 test xanh | pytest `test_a_*` … `test_f_*` | Functional |
| TC-015 | Không tìm thấy | US-005-AC1, AC2, AC-008, FR-011, MET-004 | P0 | Đã đưa mẫu | 1. Hỏi 5 câu âm tính | G-51..G-55 | Câu cố định, sources rỗng; ≥ 90 % | pytest `test_not_found_has_fixed_sentence_and_no_sources`; golden | Negative |
| TC-016 | Văn bản sắp có hiệu lực | US-006-AC1, AC-013, AC-015, FR-010 | P1 | Đã đưa mẫu | 1. Hỏi số ngày phép năm | G-12 | Dòng đầu 12 ngày; "sắp có hiệu lực từ 01/01/2027", 14 ngày | pytest `test_future_rule_is_announced_not_applied`; golden G-12 | Functional |
| TC-017 | Một bản ghi số liệu, không có nội dung | US-007-AC1, AC-010, FR-014 | P0 | Đã đưa mẫu | 1. Hỏi 1 câu 2. Đọc ask_log | — | 1 dòng: id, at, latency_ms, status, cited_count | pytest `test_ask_returns_sources_and_one_usage_record_without_text` | Functional |
| TC-018 | Không lộ nội dung trong log và CSDL | US-007-AC2, AC-011, NFR-003, RC-4 | P0 | Golden set đã chạy | 1. Tìm 17 câu hỏi trong app.log và golden.db | — | 0 kết quả | `leak-check.txt`, golden summary "NFR-003 leaks: []" | Security |
| TC-019 | Lỗi thành phần trả lời → 503, có bản ghi error | US-007-AC3, US-010-AC1, FR-015 | P0 | Answerer bị thay bằng hàm lỗi | 1. Hỏi | — | 503 ai_unavailable; ask_log status = error | pytest `test_answerer_failure_is_503_and_logged_as_error` | Negative |
| TC-020 | Lỗi ghi số liệu vẫn trả lời | US-007-AC4, FR-017 | P1 | UsageLog lỗi | 1. Hỏi | — | 200, found = true | pytest `test_usage_log_failure_still_answers` | Negative |
| TC-021 | Chỉ dẫn trong văn bản bị bỏ qua | US-008-AC1, AC-012, FR-012 | P0 | Đã đưa mẫu (có TB 09/2026) | 1. Kiểm units_filtered 2. Hỏi phụ cấp | — | units_filtered = 1; không có "1 tỷ" | pytest `test_injected_instruction_is_dropped`, `test_injected_instruction_never_answers`; golden G-05, G-09 | Security |
| TC-022 | Chưa có văn bản: khóa ô hỏi | US-009-AC1, FR-013 | P1 | Kho trống | 1. Mở trang Tra cứu 2. Gọi /api/ask | — | Ô hỏi khóa + hướng dẫn; API 409 no_documents | pytest `test_no_documents_then_upload_then_list`; UI `ui-locked.png` | Functional |
| TC-023 | Hỏi lại sau khi bận | US-010-AC2, FR-015 | P1 | UI | 1. Kiểm tra code `web/app.js` (nút retry gọi lại cùng câu hỏi) | — | retry gọi `ask(question, turn)` | `inspection.md` | Inspection |
| TC-024 | p90 ≤ 30 s | NFR-001, MET-006, AC-009 | P0 | Golden set | 1. Chạy run_golden.py | — | p90 ≤ 30000 ms | golden summary | Performance |
| TC-025 | 10 câu đồng thời | NFR-006 | P0 | Đã đưa mẫu | 1. 10 luồng cùng hỏi | — | 10 × 200 | pytest `test_ten_concurrent_questions` | Performance |
| TC-026 | Văn bản 20 trang sẵn sàng ≤ 60 s | NFR-002 | P0 | — | 1. Đưa PDF 20 trang, đo thời gian | `many_pages_pdf(20)` | ≤ 60 s | `perf.txt` | Performance |
| TC-027 | Chỉ nghe localhost; HTTPS khi triển khai; không mã hóa trong capstone | NFR-004, NFR-008, NFR-009, AC-014 | P0 | — | 1. Đọc lệnh chạy và SAD §4.1, §4.5 | — | uvicorn `--host 127.0.0.1`; ghi rõ hướng dẫn triển khai | `inspection.md` | Inspection |
| TC-028 | Diễn tập phục hồi | NFR-005 | P1 | — | 1. Xóa CSDL 2. Đưa lại 5 văn bản 3. Đo thời gian | — | Toàn bộ Sẵn sàng; thời gian ≪ 1 ngày | `recovery.txt` | Reliability |
| TC-029 | Giao diện tiếng Việt | NFR-007 | P1 | UI | 1. Xem hai màn hình | — | Không có chuỗi tiếng Anh hiển thị cho người dùng | `ui-*.png`, `web/vi.json` | Inspection |
| TC-030 | Lint, kiến trúc phụ thuộc | RC-1, SAD §2.3 | P0 | — | 1. ruff 2. test import rules | — | 0 lỗi; 2 test xanh | `ruff.txt`, pytest `test_only_wiring_imports_adapters` | Static |

**Coverage:** xem `RTM.md`.
