# Test audit — TEST_PLAN / TEST_CASES / RTM / TEST_REPORT

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-TA-001 |
| Date | 2026-11-02 |
| Auditor | checklist-auditor sub-agent |
| Artifacts | `TEST_PLAN.md` (TCQC-TP-001 v1.0), `TEST_CASES.md` (TCQC-TC v1.0), `RTM.md` (TCQC-RTM v1.0), `TEST_REPORT.md` (TCQC-TSR-001 v1.0) |
| Evidence | `evidence/20261102-2306-8ae514b-local-win/` |
| Checklist | `sdlc-kit/verification/Test_Plan_IEEE_829_Checklist.xlsx` (kit commit `26ec9ff`) |
| Prompts | `TestPlan_IEEE 829-2008_prompt.md`, `TestCase_RTM_IEEE_829_Prompt.md`, `TestReport_IEEE_829_Prompt.md` |
| Upstream | `analysis-v1`, `design-v1`, `plan-v1` |

## 1. Bảng chấm checklist (áp cho TEST_PLAN)

| # | Category | Checklist Item | Status | Evidence | Notes / Action Items | Owner | Gate |
|---|---|---|---|---|---|---|---|
| 1 | 1. Document Metadata | Test Plan Identifier | Pass | Bảng đầu: TCQC-TP-001 v1.0, prompt v2.0 | — | QA lead | Non-blocking |
| 2 | 1. Document Metadata | Introduction | Pass | §2.0 | — | QA lead | Non-blocking |
| 3 | 2. Scope & Features | Test Items | Pass | §3.0 (`app/`, `web/`, fixtures, golden) | — | QA lead | Non-blocking |
| 4 | 2. Scope & Features | Features to be Tested | Pass | §4.0, US-001..010 + NFR | — | QA lead | Non-blocking |
| 5 | 2. Scope & Features | Features Not to be Tested | Pass | §5.0 (PRD §1.3, MET-001/005, LLM ngoài) | — | QA lead | Non-blocking |
| 6 | 3. Approach & Methodology | Testing Approach | Pass | §6.0 bảng mức + lệnh | — | QA lead | Non-blocking |
| 7 | 3. Approach & Methodology | Automation vs Manual | Partial | §6.0 | Ghi rõ tự động (pytest, golden) vs thủ công/agent (UI, inspection, diễn tập). Hạn 2026-11-09 | QA lead | Non-blocking |
| 8 | 4. Pass/Fail & Lifecycle | Item Pass/Fail Criteria | Pass | §7.0 RC-1..RC-6 có ngưỡng đo được | Thiếu entry criteria tường minh (prompt §6) — bổ sung | QA lead | Non-blocking |
| 9 | 4. Pass/Fail & Lifecycle | Suspension Criteria | Pass | §8.0 | — | QA lead | Non-blocking |
| 10 | 4. Pass/Fail & Lifecycle | Resumption Requirements | Pass | §8.0 (chạy lại toàn bộ, run-id mới); đã áp dụng thật (TEST_REPORT §3, DEF-001) | — | QA lead | Non-blocking |
| 11 | 5. Environment & Resources | Environmental Needs | Pass | §11.0, §6.0 (`TCQC_TODAY`) | — | QA lead | Non-blocking |
| 12 | 5. Environment & Resources | Responsibilities | Pass | §12.0 (agent thực thi, PO duyệt/ký) | — | PO | Non-blocking |
| 13 | 5. Environment & Resources | Staffing & Training Needs | Partial | §12.0/13.0 gộp, không nói nhu cầu đào tạo | Ghi "không cần đào tạo" hoặc kiến thức cần (quy chế nội bộ để duyệt golden). Hạn 2026-11-09 | PO | Non-blocking |
| 14 | 6. Execution & Delivery | Testing Tasks | Partial | §10.0 liệt kê 7 bước, không gán người | Gán vai trò cho từng bước. Hạn 2026-11-09 | QA lead | Non-blocking |
| 15 | 6. Execution & Delivery | Test Deliverables | Partial | §9.0 ghi `ui-*.png`, thiếu `perf.txt`, `ui-*.txt`, `golden-console.txt` | Sửa đúng tên/đuôi tệp thực tế (`.jpg`). Hạn 2026-11-09 | QA lead | Non-blocking |
| 16 | 6. Execution & Delivery | Schedule | Pass | §14.0 (SDP MS-4) | — | PO | Non-blocking |
| 17 | 7. Risk Management | Risks & Contingencies | Pass | §15.0 RSK-002, RSK-005 | Chưa nêu thứ tự test theo rủi ro (prompt §6) | QA lead | Non-blocking |
| 18 | 7. Risk Management | Approvals | Pass | §16.0; bảng ký ở TEST_REPORT §7 | — | PO | Non-blocking |

**Tổng:** Pass 14 · Partial 4 · Fail 0 · N/A 0.

## 2. Đối chiếu số liệu với bằng chứng

| Khẳng định | Nguồn | Có trong bằng chứng? |
|---|---|---|
| pytest 46 passed | `pytest.txt` dòng cuối "46 passed, 1 warning"; 46 dòng PASSED | Có |
| ruff 0 lỗi | `ruff.txt` "All checks passed!" | Có |
| Golden 17/17 | `golden-console.txt` G-01..G-12, G-51..G-55 PASS, "RC-2: PASS" | Có |
| MET-002 12/12, MET-003 3/3, future 1/1, MET-004 5/5, MET-007 8/8, p90 18,2 ms, leaks [] | `golden-results.json` summary | Có, khớp |
| NFR-002 0,13 s | `perf.txt` | Có |
| NFR-005 5 văn bản, 0,18 s | `recovery.txt` | Có |
| NFR-003 0 lộ (17 golden + 2 UI) | `leak-check.txt` (2 dòng UI False, golden leaks []) | Có |
| UI: căn cứ, xung đột, không tìm thấy, khóa ô hỏi | `ui-answer.txt`, `ui-documents.txt`, `ui-upload-response.txt` | Có |
| Mọi tên test pytest được trích trong RTM/TEST_CASES | grep `pytest.txt` (kể cả test_a..test_f, CR-R-01/02, DEF-001) | Có, đủ |
| **"22/22 test case P0 PASS"** (RTM, TEST_REPORT §1, RC-3) | `TEST_CASES.md`: **24** case P0, 6 case P1 | **Không khớp** — số đúng là 24/24 (cả 24 đều PASS trong RTM) |

## 3. Vi phạm self-check / anti-pattern của prompt

| # | Phát hiện | Mức | Action | Owner | Gate |
|---|---|---|---|---|---|
| F-1 | Số P0 khai 22/22, thực tế 24 (RTM coverage, TEST_REPORT §1, §4 RC-3) | Partial | Sửa thành 24/24; kết luận RC-3 không đổi vì cả 24 PASS | QA lead | Non-blocking (sửa trước khi PO ký) |
| F-2 | TC-029 PASS trong khi expected "không có chuỗi tiếng Anh" bị DEF-002 vi phạm (`inspection.md` ghi "PASS with DEF-002") | Partial | Đổi thành FAIL (P1, Minor) hoặc ghi rõ deviation được PO chấp nhận | QA lead / PO | Non-blocking (P1, không ảnh hưởng RC-3) |
| F-3 | Evidence ghi `ui-*.png` (TEST_CASES TC-002, 006, 008, 022, 029; TEST_PLAN §9) nhưng tệp là `.jpg` | Partial | Sửa đuôi tệp | QA lead | Non-blocking |
| F-4 | TEST_PLAN §6.0 diễn tập "đưa lại 3 văn bản", thực tế 5 (`recovery.txt`) | Partial | Đồng bộ con số | QA lead | Non-blocking |
| F-5 | TEST_PLAN không báo điểm self-check (prompt §6 bước 7) và không có entry criteria / thứ tự test theo rủi ro | Partial | Thêm mục self-check score, entry criteria, thứ tự test | QA lead | Non-blocking |

Không có khẳng định kết quả nào thiếu bằng chứng gốc; MET-001 GAP và US-002-AC3 SKIP đều có lý do, owner, hạn.

## 4. Blocking items

Không có.

## 5. Verdict

**Gate ready** (0 Fail). Khuyến nghị sửa F-1..F-5 trước khi PO ký RC-6. Auditor không phê duyệt; PO quyết định.


## Quyết định tại cổng (2026-11-02)

PO duyệt có điều kiện; điều kiện đạt (0 Fail, 0 Blocking). Trước khi ký đã sửa F-1..F-5: P0 = 24/24; TC-029 → FAIL do DEF-002; đuôi `.jpg`; diễn tập 5 văn bản; Test Plan bổ sung automation/manual, thứ tự theo rủi ro, điều kiện bắt đầu, vai trò, self-check. Baseline `verification-v1`.
