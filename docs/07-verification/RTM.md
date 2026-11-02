# RTM — Requirements Traceability Matrix

| Mục | Giá trị |
|---|---|
| ID | TCQC-RTM, version 1.0 |
| Owner | Phùng Duy Hùng (PO) |
| Tested commit | `8ae514b` (nhánh `restart`; các commit sau chỉ đổi tài liệu) |
| Environment | Windows 10 Pro 19045, Python 3.13, localhost; `TCQC_TODAY=2026-11-02` |
| Run id | `20261102-2306-8ae514b-local-win` → bằng chứng ở [evidence/20261102-2306-8ae514b-local-win/](evidence/20261102-2306-8ae514b-local-win/) (gọi tắt `ev/`) |
| Date | 2026-11-02 |
| Prompt | `sdlc-kit/verification/TestCase_RTM_IEEE_829_Prompt.md` v2.0 |

Chuỗi truy vết đầy đủ:
- BO → BR: [BRD §4.11](../02-requirements/BRD.md);
- BR → FR → US: [traceability.md](../03-analysis/traceability.md);
- US/AC → TC → evidence: bảng dưới.

| Acceptance criterion | Requirement | Story | Test case | Result | Evidence | Defect | Notes |
|---|---|---|---|---|---|---|---|
| US-001-AC1 / AC-001: 3 văn bản → Sẵn sàng | FR-001 (BR-001) | US-001 | TC-001 | PASS | `ev/pytest.txt` test_three_valid_documents_become_ready; `ev/ui-upload-response.txt` | — | |
| US-001-AC2: 11 tệp bị chặn trước khi gửi | FR-001 | US-001 | TC-002 | PASS | `ev/ui-too-many.jpg`, `ev/ui-answer.txt`; pytest test_eleven_files_is_400 | — | |
| US-001-AC3 / AC-002: một lý do mỗi tệp | FR-002 (BR-002) | US-001 | TC-003 | PASS | pytest test_bad_files_get_one_reason_each…; `ev/ui-upload-response.txt` | DEF-003 | |
| US-001-AC4, AC5: trùng tên, > 20 MB, > 300 trang | FR-002, NFR-010 | US-001 | TC-004 | PASS | pytest test_duplicate_too_large_too_many_pages | — | |
| US-001-AC6: kho đầy | FR-016 | US-001 | TC-005 | PASS | pytest test_collection_full | — | Giới hạn đặt = 2 trong test |
| US-002-AC1, AC2 / AC-003: số hiệu, hiệu lực, "kể từ ngày ký" | FR-003, FR-004 (BR-003) | US-002 | TC-006, TC-007 | PASS | `ev/ui-documents.txt`, `ev/ui-documents.jpg`; pytest test_metadata_*, test_effective_from_signing… | — | |
| US-002-AC3: tự cập nhật ≤ 5 s | FR-018 | US-002 | — | SKIP | — | — | Xử lý đồng bộ (ADR-004, OQ-008): không có trạng thái Đang xử lý kéo dài để quan sát. Code `web/app.js` loadDocs() hẹn 3 s khi processing > 0. Người duyệt SKIP: PO |
| US-002-AC4: văn bản chưa Sẵn sàng không làm căn cứ | FR-005 | US-002 | TC-006 | PASS | `ready_units()` chỉ lấy status = ready; pytest test_three_valid…, test_bad_files… (tệp lỗi không có unit) | — | |
| US-003-AC1, AC2 / AC-005: căn cứ đủ thành phần | FR-007, FR-008, FR-019 (BR-005) | US-003 | TC-008 | PASS | pytest test_positive_answer_has_reference_and_full_source; `ev/ui-answer.txt` | — | |
| US-003-AC3: câu hỏi không hợp lệ | FR-006 | US-003 | TC-009 | PASS | pytest test_invalid_question_is_422 ×3 | — | |
| US-003-AC4 / AC-004, AC-016: MET-002, MET-007 | FR-007 (BR-004, BR-016) | US-003 | TC-010 | PASS | `ev/golden-results.json`: MET-002 12/12, MET-007 8/8 | — | PO duyệt kết quả chấm tự động trong TEST_REPORT |
| US-004-AC1, AC2 / AC-006, AC-007 | FR-009, FR-020 (BR-006, BR-007) | US-004 | TC-011 | PASS | pytest test_conflict_names…; golden G-09; `ev/ui-answer.txt` | — | |
| US-004-AC3: MET-003 | FR-009 | US-004 | TC-012, TC-013, TC-014 | PASS | golden G-09..G-11 3/3, G-07; pytest test_a…test_f | — | |
| US-005-AC1, AC2 / AC-008: MET-004 | FR-011 (BR-008) | US-005 | TC-015 | PASS | golden G-51..G-55 5/5; `ev/ui-answer.txt` | — | |
| US-006-AC1 / AC-013, AC-015 | FR-010 (BR-013, BR-015) | US-006 | TC-016 | PASS | golden G-12; pytest test_future_rule_is_announced_not_applied, test_c_future… | — | |
| US-007-AC1 / AC-010 | FR-014 (BR-010) | US-007 | TC-017 | PASS | pytest test_ask_returns_sources_and_one_usage_record_without_text | — | |
| US-007-AC2 / AC-011 | NFR-003 (BR-011) | US-007 | TC-018 | PASS | `ev/leak-check.txt`, golden summary "NFR-003 leaks: []" | — | |
| US-007-AC3; US-010-AC1 | FR-014, FR-015 | US-007, US-010 | TC-019 | PASS | pytest test_answerer_failure_is_503…, test_timeout_is_503_and_logged | — | |
| US-007-AC4 | FR-017 | US-007 | TC-020 | PASS | pytest test_usage_log_failure_still_answers | — | |
| US-008-AC1 / AC-012 | FR-012 (BR-012) | US-008 | TC-021 | PASS | pytest test_injected_instruction_is_dropped, …never_answers; golden G-05, G-09 (không chứa "1 tỷ") | — | |
| US-009-AC1 | FR-013 | US-009 | TC-022 | PASS | `ev/ui-locked.jpg`, `ev/ui-answer.txt`; pytest test_no_documents_then_upload… | — | |
| US-010-AC2 | FR-015 | US-010 | TC-023 | PASS | `ev/inspection.md` | — | Inspection |
| AC-009: p90 ≤ 30 s | NFR-001 (BR-009) | — | TC-024 | PASS | golden p90 = 18,2 ms | — | |
| NFR-006: 10 câu đồng thời | NFR-006 | — | TC-025 | PASS | pytest test_ten_concurrent_questions, test_rebuild_during_questions_never_fails | — | |
| NFR-002: 20 trang ≤ 60 s | NFR-002 | — | TC-026 | PASS | `ev/perf.txt` (0,13 s) | — | |
| AC-014: chỉ mạng nội bộ | NFR-004, NFR-008, NFR-009 (BR-014) | — | TC-027 | PASS | `ev/inspection.md` | — | Inspection |
| NFR-005: phục hồi | NFR-005 | — | TC-028 | PASS | `ev/recovery.txt` | DEF-001 (đã sửa) | Lần chạy đầu phát hiện DEF-001 |
| NFR-007: tiếng Việt | NFR-007 | — | TC-029 | FAIL | `ev/ui-too-many.jpg` ("Choose Files"), `ev/inspection.md` | DEF-002 | P1. Mọi chuỗi của ứng dụng đều tiếng Việt; chỉ nút gốc của trình duyệt còn tiếng Anh |
| RC-1: lint, kiến trúc | — | — | TC-030 | PASS | `ev/ruff.txt`, `ev/pytest.txt` (46 passed) | — | |
| MET-001: người dùng ≤ 2 phút | BR-009 (BO-001) | — | — | GAP | — | — | Cần bấm giờ với người dùng thật (deferred). Owner: PO; hạn 2026-11-30 (cùng OQ-001) |

**Coverage summary:**

| | Số lượng |
|---|---|
| Tiêu chí | 30 |
| PASS | 27 |
| FAIL | 1 (TC-029, P1, DEF-002 Minor) |
| SKIP | 1 (US-002-AC3, có lý do) |
| GAP | 1 (MET-001, có owner và hạn) |
| Test case P0 | 24/24 PASS |

Mọi BR-001..016 đều có ít nhất một tiêu chí PASS. Không có test case nào không truy được về yêu cầu.
