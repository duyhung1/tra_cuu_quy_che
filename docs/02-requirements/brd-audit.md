# BRD audit — TCQC-BRD v0.1

## Document control

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-BRD-AUDIT-01 |
| Ngày | 2026-11-02 |
| Auditor | checklist-auditor sub-agent |
| Artifact | `docs/02-requirements/BRD.md` — TCQC-BRD, version 0.1, status `In review` |
| Checklist | `sdlc-kit/analysis/BRD_IEEE_29148_Checklist.xlsx` (20 dòng), kit commit `6996dae` |
| Prompt sinh artifact | `sdlc-kit/analysis/BRD_Prompt_IEEE_standard.md` v2.0; tham số `prompts/02-requirements.md` |
| Đầu vào đối chiếu | `docs/01-intake/` (intent.md, sources.md, stakeholders.md, glossary.md, work-item.md — baseline `intake-v1`), `docs/02-requirements/interviews/SRC-005.md` |
| Phương pháp | `sdlc-kit/step-by-step-guidance.md` §A8. Mọi bằng chứng được mở lại ở nguồn; không dựa vào tự đánh giá của BRD |
| Người duyệt | Phùng Duy Hùng (PO). Auditor không duyệt |

Ghi chú: dự án chỉ có một người (PO) nên mọi Owner là PO; BRD do agent soạn, agent sửa theo chỉ đạo của PO nhưng PO chịu trách nhiệm đóng mục. Hạn chung: cổng BRD 2026-11-02.

## Bảng chấm

| # | Category | Checklist Item | Status | Evidence | Notes / Action Items | Owner | Gate |
|---|---|---|---|---|---|---|---|
| 1 | 1. Document & Business Overview | Business Purpose & Drivers | Pass | §4.2 dòng 25–26; §4.3 "Nguyên nhân gốc" dòng 67, "Vì sao làm bây giờ" dòng 68; §4.4 BO-001..004 cột Business driver. Khớp intent.md §1 | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 2 | 1. Document & Business Overview | Business Objectives & Success Metrics | Partial | §4.4 MET-001..005 (dòng 79–85). MET-001 dòng 81 gộp hai phép đo ("p90 độ trễ hệ thống; trung bình thời gian bấm giờ 5 câu") với hai target (≤ 2 phút; p90 ≤ 30 giây, dòng 74). MET-002..004 baseline và ngày baseline "Chưa có", không có hành động đo. Golden set không nêu cỡ / thành phần nên tỷ lệ ≥ 80 %, 100 %, ≥ 90 % không xác định được mẫu số. ROI: ngân sách "không công bố" (dòng 32) — chấp nhận được cho dự án học tập | (a) Tách MET-001 thành hai metric (độ trễ hệ thống p90 và thời gian người dùng bấm giờ) hoặc nêu rõ target nào là tiêu chí nghiệm thu; (b) ghi baseline MET-002..004 là "không áp dụng — năng lực mới" kèm lý do, hoặc thêm cách đo baseline tra tay; (c) nêu số câu tối thiểu mỗi loại (dương tính / xung đột / âm tính) của golden set hoặc mở OQ. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 3 | 1. Document & Business Overview | Scope & Boundaries | Pass | §4.5: In scope dòng 91–96; Out of scope có lý do dòng 100–107 (đủ 6 mục của intent.md §6, thêm DOCX từ SRC-005 Q8); Deferred dòng 109 (gồm đo SM-05/MET-005); Boundaries dòng 111 | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 4 | 1. Document & Business Overview | Vision Statement | Partial | Không có mục / câu vision riêng. §4.2 "Thay đổi đề xuất" (dòng 26) mô tả năng lực nhưng không gắn với chiến lược tổ chức. `SUCCESS_IN_SPONSOR_WORDS` ("Hỏi là có câu trả lời kèm căn cứ Điều/Khoản đúng văn bản đang hiệu lực", `prompts/02-requirements.md` dòng 20) không được dùng | Thêm 1–2 câu vision ở §4.2 (dùng lời của sponsor) và nêu nó phục vụ mục tiêu nào của tổ chức (giảm sai sót chi tiêu, giảm tải HC-NS). Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 5 | 2. Stakeholder & User Analysis | Stakeholder Identification | Pass | §4.6 STK-01..05 (dòng 117–121), có người có thể cản nghiệm thu (STK-05). STK-06 (AI agent, stakeholders.md dòng 19) bị bỏ mà không ghi lý do | Ghi một dòng ở §4.6 vì sao STK-06 không phải stakeholder nghiệp vụ (giữ ID, không xóa ngầm). Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 6 | 2. Stakeholder & User Analysis | User Personas & Profile Characteristics | Partial | §4.6 chỉ có vai trò / quan tâm. Không có bối cảnh dùng (intent.md §3: "khi đi công tác, nghỉ phép, thanh toán"), tần suất, mức hiểu biết quy chế, số người (OQ-003 có trong §4.12 nhưng không được nhắc ở §4.6) | Thêm bảng hồ sơ người dùng ngắn cho STK-02..04: tình huống tra cứu điển hình, tần suất, mức hiểu Điều/Khoản, số lượng `[TBD: OQ-003]`. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 7 | 2. Stakeholder & User Analysis | Business Constraints | Pass | §4.9 CON-01..07 khớp intent.md §4 (Time, Organizational); ngân sách §4.2 dòng 32; pháp lý §4.10 dòng 216 | Không cần hành động (xem mục 15 về trích nguồn) | PO (Phùng Duy Hùng) | Non-blocking |
| 8 | 3. Business Process & Operational Concept | Current State ('As-Is') Workflow | Pass | §4.3 sơ đồ As-Is dòng 39–48, khớp intent.md §1. Bước "Tìm văn bản liên quan trong thư mục chung" (dòng 41) không có trong nguồn nào | Gắn `[Unverified]` cho "thư mục chung" hoặc bỏ chi tiết này. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 9 | 3. Business Process & Operational Concept | Target State ('To-Be') Workflow | Partial | §4.3 sơ đồ To-Be dòng 52–60: thiếu nhánh "không tìm thấy" (BR-008), "sắp có hiệu lực" (BR-013) và văn bản lỗi (BR-002). Nút H dòng 59 ghi "Hành chính – nhân sự đưa văn bản mới vào", trái với BR-001 và OQ-002 đã trả lời (intent.md dòng 76: mọi người dùng nội bộ) | Bổ sung ba nhánh trên; đổi nút H thành "Người dùng nội bộ đưa văn bản vào". Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 10 | 3. Business Process & Operational Concept | Operational Scenario & Use Cases | Partial | Không có mục kịch bản nghiệp vụ. Chỉ có sơ đồ §4.3 và AC §4.7 (dòng 164–179) mang tính kiểm thử, không phải kịch bản từ phía người dùng | Thêm 3–4 kịch bản ngắn: nhân viên tra công tác phí; kế toán kiểm căn cứ hồ sơ có quyết định sửa đổi; câu hỏi ngoài phạm vi; HC-NS đưa văn bản mới có tệp lỗi. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 11 | 4. Business & High-Level Functional Requirements | Singularity & Clarity | Partial | Mọi BR dùng "shall" (§4.7 dòng 137–160). Vấn đề: BR-013 (dòng 151) gộp hai nghĩa vụ ("nêu 'sắp có hiệu lực'" và "không dùng nó thay cho quy định đang áp dụng" — phần sau trùng BRU-003); BR-009 (dòng 150) trỏ tới MET-001 có hai target nên mơ hồ (AC-009 chỉ kiểm p90 ≤ 30 giây); thuật ngữ chưa có trong glossary: "golden set", "câu dương tính / âm tính", "câu xung đột", "quy tắc trả lời" (BR-012), "PDF có lớp văn bản", viết tắt "HC-NS" | Tách BR-013 thành BR-013 (nêu "sắp có hiệu lực") và dựa vào BRU-003 cho phần còn lại; viết BR-009 với một con số cụ thể; bổ sung các thuật ngữ trên vào §4.13 (hoặc đề xuất sửa glossary qua change control). Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 12 | 4. Business & High-Level Functional Requirements | Completeness & Implementation-Free | Partial | BR không nêu công nghệ (Pass phần implementation-free; DEP-001 dòng 211 đặt công nghệ đúng chỗ). Thiếu sót: BO-004 / SN-02 không có BR nào (§4.11 dòng 225); BRU-004, BRU-005 (dòng 188–189) không có BR/AC nào kiểm; glossary định nghĩa "Căn cứ" gồm cả trang (glossary.md dòng 23) nhưng BR-005 (dòng 146) không có trang; BR-007 là Should (dòng 148) trong khi WI-AC-03 (work-item.md dòng 29) coi việc nêu văn bản bị thay thế là tiêu chí chấp nhận của work item; AC-007 (dòng 172) chỉ kiểm "văn bản", không kiểm "quy định" bị thay thế như BR-007 | (a) Ghi rõ BO-004 không có BR trong phiên bản này kèm lý do, hoặc thêm BR; (b) thêm AC cho giới hạn BRU-004 và luật BRU-005 (hoặc nêu chúng được kiểm qua BR-002); (c) thống nhất BR-005 với định nghĩa "Căn cứ" (thêm trang hoặc đề xuất sửa glossary); (d) nâng BR-007 lên Must hoặc ghi PO chấp nhận lệch với WI-AC-03; (e) sửa AC-007 cho khớp BR-007. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 13 | 4. Business & High-Level Functional Requirements | Traceability & Rationale | Partial | Mọi BR có ID, rationale, source (§4.7). BR-011 (dòng 158) và BR-014 (dòng 160) chỉ trỏ tới CON-03 / CON-05, không tới BO/SN — prompt §7.1 yêu cầu nguồn là `BO-xxx`/`SN-xxx`. Ma trận §4.11 lệch bảng BR: BR-012 nằm dưới BO-003 nhưng bảng BR không cite BO-003; BR-003 cite SN-04 nhưng ma trận chỉ ghi SN-03. Thiếu báo cáo coverage bắt buộc (prompt §7.2 4.11: objective không có BR, BR mồ côi, need không có BR, BR thiếu AC/verification) và cột downstream PRD/SRS ID | Gắn BR-011, BR-014 vào SN/BO phù hợp (ví dụ SN-04 / STK-01) hoặc chuyển thành constraint; đồng bộ ma trận với cột Source; thêm danh sách coverage bốn mục (nêu rõ BO-004 và SN-02 chưa có BR) và cột downstream = `TBD`. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 14 | 4. Business & High-Level Functional Requirements | Feasibility & Realism | Pass | 14 BR, phạm vi đã cắt theo CON-01 (§4.9 dòng 195); RSK-002 (dòng 213) có biện pháp cắt bề rộng; DEP-001 (dòng 211) được nêu là phụ thuộc chính | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 15 | 5. Business Quality & Non-Functional Attributes | Compliance & Regulatory Standards | Pass | §4.10 dòng 216: không có quy định pháp lý vì dữ liệu giả lập, khớp `REGULATORY_CONTEXT: "none"` (`prompts/02-requirements.md` dòng 22, `prompts/01-intake.md` dòng 20); quyền riêng tư CON-02; khả năng kiểm tra BR-010, BR-011. Trích nguồn "[Source: intake §2.2 REGULATORY_CONTEXT]" không mở được trong `docs/01-intake/` | Sửa trích dẫn thành `prompts/01-intake.md` / `prompts/02-requirements.md` `REGULATORY_CONTEXT`. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 16 | 5. Business Quality & Non-Functional Attributes | Business Continuity & Availability | Partial | Chỉ có ASM-003 (dòng 209) và "Continuity: theo ASM-003" (dòng 216). Khung giờ "08:00–17:30, thứ Hai–thứ Sáu" của SRC-005 P2 bị bỏ, chỉ còn "giờ hành chính". Không nêu mục tiêu khôi phục kho văn bản / mất dữ liệu (RPO). ASM-003 chưa được PO xác nhận (OQ-005) | Ghi khung giờ đầy đủ; thêm kỳ vọng về mất dữ liệu kho văn bản (ví dụ "đưa lại văn bản là chấp nhận được") dưới dạng ASM; xác nhận cùng OQ-005. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 17 | 5. Business Quality & Non-Functional Attributes | Security & Business Policy Constraints | Pass | BR-014 (dòng 160), BR-011 (dòng 158), BR-012 (dòng 159) + RSK-003 (dòng 214); không đăng nhập là quyết định của PO (§4.5 dòng 102, SRC-005 Q7) | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 18 | 6. Assumptions, Dependencies & Risks | Business Assumptions | Partial | ASM-001..004 (dòng 207–210) đủ owner, cách xác nhận, hạn. Nhưng đề xuất chưa xác nhận lại được ghi như quyết định: BRU-003 (Policy, dòng 187) và BRU-004 (Decision, dòng 188) lấy từ SRC-005 P3, P1 — SRC-005 dòng 29 ghi "nếu chưa xác nhận thì chúng là `ASM`". BRU-005 (dòng 189) cite SRC-005 Q7 nhưng câu trả lời của PO ở Q7 (SRC-005 dòng 23) chỉ nói "Mọi người dùng nội bộ; không có đăng nhập", không có gì về tên tệp trùng — luật này là suy luận của BA, không có nguồn, và cũng không nằm trong OQ-005 | Đánh dấu BRU-003, BRU-004 `[Unverified: OQ-005]` cho đến khi PO xác nhận; thêm BRU-005 vào OQ-005 (hoặc chuyển thành ASM) và sửa nguồn; PO xác nhận / sửa P1–P3 và BRU-005 tại cổng. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | **Blocking** |
| 19 | 6. Assumptions, Dependencies & Risks | Dependencies & Constraints | Partial | Chỉ có DEP-001 (dòng 211). Thiếu: bộ văn bản mẫu có trường hợp xung đột và văn bản hiệu lực tương lai (cần cho AC-006, AC-013); golden set và người chấm (MET-002..004, AC-004 "PO chấm"); hạ tầng mạng nội bộ cho BR-014; PO sẵn sàng trả lời OQ-005 trong ngày | Thêm DEP cho văn bản mẫu, golden set, mạng nội bộ, kèm owner và hạn. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 20 | 6. Assumptions, Dependencies & Risks | Business Risks & Mitigation | Partial | RSK-001..003 (dòng 212–214) có mitigation. Thiếu mức nghiêm trọng (prompt §7.2 4.10 "Impact if false = Severity"), thiếu kế hoạch dự phòng (contingency), không theo dạng cause → event → effect. Không có rủi ro về việc gửi nội dung văn bản cho dịch vụ bên ngoài (DEP-001), dù CON-02 giảm nhẹ | Thêm severity và contingency cho từng RSK; thêm rủi ro gắn với DEP-001 (nhà cung cấp không sẵn sàng / không được phép nhận nội dung). Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |

## Tóm tắt

| Pass | Partial | Fail | N/A | Tổng |
|---|---|---|---|---|
| 8 | 12 | 0 | 0 | 20 |

**Blocking:**

- Mục 18 (Business Assumptions): BRU-003, BRU-004 là đề xuất chưa xác nhận (OQ-005); BRU-005 không có nguồn từ PO và không nằm trong OQ-005.

## Kiểm theo §6 self-check và §7.3 / §7.4 của prompt

### §6 self-check

| Mục | Kết quả | Bằng chứng |
|---|---|---|
| Mỗi BO có ít nhất một BR và một metric đo được | **Vi phạm** | BO-004 không có BR (§4.11 dòng 225) |
| Mỗi BR dùng `shall`, một nghĩa vụ, không ngôn ngữ giải pháp | **Vi phạm một phần** | BR-013 gộp hai nghĩa vụ (dòng 151) |
| Mỗi BR có AC và phương pháp kiểm | Đạt | §4.7 cột AC, Verification; AC-001..014 |
| Mỗi BR truy về BO hoặc SN, không mồ côi | **Vi phạm một phần** | BR-011, BR-014 chỉ truy về CON (dòng 158, 160); §4.11 dòng 230 tự mở rộng quy tắc thành "BO / SN / CON" |
| Scope, exclusions, assumptions, dependencies, risks đều có | Đạt | §4.5, §4.10 |
| Mỗi OQ có owner và hạn | Đạt | §4.12 dòng 236–238 |
| Sponsor xác nhận problem và outcome | Chưa | §4.14 dòng 249 "(chờ)" — việc của PO tại cổng |
| Điểm checklist được báo cáo kèm artifact | **Vi phạm** | BRD không có bảng tự chấm; chỉ có câu Readiness dòng 255 |

### §7.3 (các mục chưa nằm trong bảng chấm)

- Glossary: thiếu "golden set", "câu dương tính / âm tính / xung đột", "sắp có hiệu lực", "PDF có lớp văn bản", "HC-NS" (§4.13 chỉ trỏ tới glossary intake).
- §4.11: không có báo cáo coverage và cột downstream ID.
- §4.12: thiếu cột "Why it matters" và "Resolution"; quyết định OQ-002, OQ-004 (intent.md dòng 76, 78) và Q7, Q8 của SRC-005 không được ghi lại như quyết định (ngày, người quyết, lý do).
- §4.13: tham chiếu thiếu phiên bản / vị trí / ngày truy cập (SOP không ghi kit commit `6996dae`).
- §4.14: không nêu điều kiện phê duyệt và phiên bản baseline được duyệt (chỉ có ở §4.2 dòng 33).
- Must requirement không đạt một check: BR-009 (mơ hồ), BR-011, BR-014 (truy vết). BRD ghi `Ready with conditions` chứ không ghi sẵn sàng phê duyệt, nên không trái quy tắc cuối §7.3, nhưng điều kiện chỉ liệt kê OQ-005.

### §7.4 anti-patterns

| Anti-pattern | Có xuất hiện? | Bằng chứng |
|---|---|---|
| Assumptions presented as facts | **Có** | BRU-003, BRU-004 (Policy / Decision) từ đề xuất P3, P1; BRU-005 không có nguồn |
| Open questions resolved silently in the text | **Có (BRU-005)** | Luật trùng tên tệp không được hỏi PO, không nằm trong OQ nào |
| "Improve … by X %" with no baseline | Một phần | MET-002..004 baseline "Chưa có", không có cách đo baseline |
| Requirements with no source | Không | Mọi BR có cột Source |
| Compound requirement | Một phần | BR-013 |
| Unverifiable wording / solution prescription | Không | — |
| Scope only by inclusion | Không | §4.5 có Out of scope, Deferred |

## Verdict

**Chưa Gate ready.** Có 0 Fail, nhưng còn 1 mục Blocking (mục 18 — OQ-005 và BRU-005) mà chính BRD cũng ghi là chặn baseline (§4.12 dòng 238, §4.15 dòng 255). 12 Partial không được tính là xong; mỗi mục có owner (PO) và hạn 2026-11-02. Khi PO xác nhận hoặc sửa P1–P3 và BRU-005, và mục 18 được đóng, BRD đạt điều kiện `Gate ready` (0 Fail, 0 Blocking). Quyết định duyệt và baseline `requirements-v1` thuộc PO; auditor không duyệt.
