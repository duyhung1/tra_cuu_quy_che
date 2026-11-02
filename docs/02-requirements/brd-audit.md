# BRD audit — TCQC-BRD v0.2 (vòng 2)

## Document control

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-BRD-AUDIT-02 |
| Ngày | 2026-11-02 |
| Auditor | checklist-auditor sub-agent |
| Artifact | `docs/02-requirements/BRD.md` — TCQC-BRD, version 0.2, status `In review` (commit `1b0547b`) |
| Checklist | `sdlc-kit/analysis/BRD_IEEE_29148_Checklist.xlsx` (20 dòng), kit commit `6996dae` |
| Prompt sinh artifact | `sdlc-kit/analysis/BRD_Prompt_IEEE_standard.md` v2.0; tham số `prompts/02-requirements.md` |
| Đầu vào đối chiếu | `docs/01-intake/` (baseline `intake-v1`, không đổi từ `4c23299`), `docs/02-requirements/interviews/SRC-005.md` (đã thêm P4) |
| Vòng trước | TCQC-BRD-AUDIT-01 (BRD v0.1), lưu trong git commit `1b0547b` |
| Phương pháp | `sdlc-kit/step-by-step-guidance.md` §A8. Mọi bằng chứng được mở lại ở nguồn; không dựa vào tự đánh giá của BRD (§4.11 Coverage, §4.15 Self-check) |
| Người duyệt | Phùng Duy Hùng (PO). Auditor không duyệt |

Ghi chú: dự án chỉ có một người (PO) nên mọi Owner là PO. Hạn chung: cổng BRD 2026-11-02. Số dòng dẫn chiếu là số dòng trong BRD.md v0.2.

## Round 1 → Round 2

| Dòng checklist | Vòng 1 | Vòng 2 | Đã sửa gì (BRD v0.2) |
|---|---|---|---|
| 2 Objectives & Success Metrics | Partial | Partial | Tách MET-001 / MET-006; baseline "Không có" có lý do; cỡ golden set dòng 108. Còn: target MET-007 và cỡ golden set là đề xuất của BA nhưng không được gắn `[Unverified]` |
| 4 Vision Statement | Partial | Pass | Vision dòng 26 |
| 5 Stakeholder Identification | Pass | Pass | Vẫn chưa ghi lý do bỏ STK-06 (ghi chú cũ) |
| 6 User Personas | Partial | Pass | Hồ sơ người dùng dòng 145–151, gắn OQ-005 |
| 8 As-Is | Pass (có ghi chú) | Pass | Bỏ "thư mục chung", thêm `[Unverified]` dòng 43 |
| 9 To-Be | Partial | Pass | Sơ đồ dòng 58–72 đủ nhánh; nút H sửa thành "Người dùng nội bộ" |
| 10 Operational Scenarios | Partial | Pass | SCN-01..05 dòng 76–82 |
| 11 Singularity & Clarity | Partial | Pass | Tách BR-013 / BR-015; BR-009 một con số; glossary bổ sung dòng 294–301 |
| 12 Completeness & Implementation-Free | Partial | Pass | BR-016 cho BO-004; AC-002 kiểm BRU-004/005; BR-005 có trang; BR-007 Must; AC-007 sửa |
| 13 Traceability & Rationale | Partial | Pass | SN-06 cho BR-011/014; ma trận + coverage + cột chiều xuống |
| 15 Compliance | Pass (có ghi chú) | Pass | Sửa trích dẫn REGULATORY_CONTEXT dòng 260 |
| 16 Business Continuity | Partial | Pass | Khung giờ dòng 244; ASM-005 (RPO) dòng 246 |
| 18 Business Assumptions | Partial — **Blocking** | Partial — Non-blocking | BRU-003/004/005 gắn `[Unverified: OQ-005]`; BRU-005 có nguồn SRC-005 P4; OQ-005 mở rộng. Còn: PO quyết OQ-005 tại cổng |
| 19 Dependencies | Partial | Pass | DEP-002..005 |
| 20 Risks | Partial | Pass | Mức độ, dự phòng, RSK-004 |

Tổng: vòng 1 = 8 Pass / 12 Partial / 0 Fail / 0 N/A, 1 Blocking → vòng 2 = 18 Pass / 2 Partial / 0 Fail / 0 N/A, 0 Blocking.

## Bảng chấm

| # | Category | Checklist Item | Status | Evidence | Notes / Action Items | Owner | Gate |
|---|---|---|---|---|---|---|---|
| 1 | 1. Document & Business Overview | Business Purpose & Drivers | Pass | §4.2 dòng 26–29; §4.3 nguyên nhân gốc dòng 86, why now dòng 87; §4.4 BO-001..004 dòng 93–96. Khớp intent.md §1 | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 2 | 1. Document & Business Overview | Business Objectives & Success Metrics | Partial | MET-001..007 dòng 100–106 đủ định nghĩa, công thức, nguồn, owner, tần suất; baseline không có đều nêu lý do (dòng 94–95); cỡ golden set dòng 108. Nhưng target MET-007 "≥ 80 % FAQ tự tra được" (dòng 96) và cỡ golden set (dòng 108) không có trong nguồn nào (SRC-002 chỉ có ~20 câu/tuần; SRC-005 P1–P4 không nói tới) và không gắn `[Unverified]`, không nằm trong OQ-005 (dòng 288) | Gắn `[Unverified: OQ-005]` cho target MET-007 và cỡ golden set, thêm chúng vào danh sách OQ-005 để PO xác nhận cùng lúc. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 3 | 1. Document & Business Overview | Scope & Boundaries | Pass | §4.5: In scope dòng 114–118; Out of scope có lý do dòng 124–129 (đủ mục của intent.md §6); Deferred dòng 131; Boundaries dòng 133 | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 4 | 1. Document & Business Overview | Vision Statement | Pass | Dòng 26: vision bằng lời sponsor (khớp `prompts/02-requirements.md` dòng 20) và mục tiêu tổ chức phục vụ | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 5 | 2. Stakeholder & User Analysis | Stakeholder Identification | Pass | §4.6 STK-01..05 dòng 139–143, có người có thể chặn nghiệm thu (STK-05). STK-06 (stakeholders.md dòng 19) vẫn bị bỏ mà không ghi lý do | Ghi một dòng ở §4.6 vì sao STK-06 (AI agent) không phải stakeholder nghiệp vụ. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 6 | 2. Stakeholder & User Analysis | User Personas & Profile Characteristics | Pass | Dòng 145–151: bối cảnh, tần suất, hiểu biết quy chế, thiết bị cho ba nhóm; ghi rõ là đề xuất BA, xác nhận cùng OQ-005, số lượng OQ-003 | Không cần hành động ngoài OQ-005 (mục 18) | PO (Phùng Duy Hùng) | Non-blocking |
| 7 | 2. Stakeholder & User Analysis | Business Constraints | Pass | §4.9 CON-01..07 dòng 230–236 khớp intent.md §4; ngân sách dòng 36; pháp lý dòng 260 | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 8 | 3. Business Process & Operational Concept | Current State ('As-Is') Workflow | Pass | Dòng 43–54; nguồn SRC-001, nơi lưu văn bản gắn `[Unverified]` | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 9 | 3. Business Process & Operational Concept | Target State ('To-Be') Workflow | Pass | Dòng 58–72: nhánh tệp lỗi (BR-002), "không tìm thấy" (BR-008), xung đột (BR-006/007), chưa hiệu lực (BR-013/015); người đưa văn bản là "người dùng nội bộ" (khớp BR-001, OQ-002) | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 10 | 3. Business Process & Operational Concept | Operational Scenario & Use Cases | Pass | SCN-01..05 dòng 78–82, phủ ba nhóm người dùng, xung đột, câu âm tính, tệp scan | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 11 | 4. Business & High-Level Functional Requirements | Singularity & Clarity | Pass | BR-001..016 (dòng 168–193) đều có "shall", mỗi BR một nghĩa vụ; BR-013 / BR-015 đã tách (dòng 182–183); BR-009 nêu một con số (dòng 181); thuật ngữ mới có trong §4.13 dòng 294–301 | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 12 | 4. Business & High-Level Functional Requirements | Completeness & Implementation-Free | Pass | BR-016 cho BO-004 (dòng 184); AC-002 kiểm BRU-004, BRU-005 (dòng 200); BR-005 có trang, khớp glossary "Căn cứ" (dòng 177); BR-007 Must, khớp WI-AC-03 (dòng 179); AC-007 kiểm cả văn bản và mức cũ (dòng 205). Không BR nào nêu công nghệ; công nghệ chỉ ở DEP-001 | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 13 | 4. Business & High-Level Functional Requirements | Traceability & Rationale | Pass | Mọi BR có ID, rationale, Source BO/SN; BR-011, BR-014 trỏ SN-06 (dòng 191, 193; SN-06 dòng 160). Ma trận dòng 264–273 có cột chiều xuống; coverage dòng 275–278 — đã đếm lại: 16 BR, 16 AC, 4/4 BO, 6/6 SN có BR. Lệch nhỏ: BR-003 cite SN-04 nhưng ma trận chỉ ghi dưới SN-03; BR-013, BR-015 chỉ cite SN-04 nhưng ma trận ghi dưới BO-002 | Đồng bộ cột Source của BR-003, BR-013, BR-015 với ma trận (ghi chú, không chặn). Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |
| 14 | 4. Business & High-Level Functional Requirements | Feasibility & Realism | Pass | 16 BR trong CON-01 (dòng 230); RSK-002 có dự phòng NO-GO có điều kiện (dòng 256); phụ thuộc DEP-001..005 có owner | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 15 | 5. Business Quality & Non-Functional Attributes | Compliance & Regulatory Standards | Pass | Dòng 260 trích `prompts/01-intake.md` REGULATORY_CONTEXT (đã mở: dòng 20 = "none"); quyền riêng tư CON-02; khả năng kiểm tra BR-010, BR-011 | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 16 | 5. Business Quality & Non-Functional Attributes | Business Continuity & Availability | Pass | ASM-003 dòng 244 (08:00–17:30, thứ Hai–thứ Sáu, ngừng ≤ 1 ngày làm việc, khớp SRC-005 P2); ASM-005 dòng 246 (khôi phục ≤ 1 ngày làm việc, RPO, khớp SRC-005 P4); dòng 260. Cả hai đang chờ OQ-005 — tính ở mục 18 | Không cần hành động ngoài OQ-005 | PO (Phùng Duy Hùng) | Non-blocking |
| 17 | 5. Business Quality & Non-Functional Attributes | Security & Business Policy Constraints | Pass | BR-011, BR-012, BR-014 (dòng 191–193); RSK-003, RSK-004 (dòng 257–258); không đăng nhập là quyết định PO (dòng 124, OQ-002 dòng 285) | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 18 | 6. Assumptions, Dependencies & Risks | Business Assumptions | Partial | ASM-001..005 dòng 242–246 đủ owner, cách xác nhận, hạn. BRU-003, BRU-004, BRU-005 (dòng 222–224) gắn `[Unverified: OQ-005]`; BRU-005 nay có nguồn SRC-005 P4 (SRC-005 dòng 36). Còn chờ: OQ-005 (dòng 288) — PO xác nhận P1–P4, ASM-003, ASM-005 và hồ sơ người dùng; §4.14 dòng 311 coi đây là điều kiện duyệt | PO quyết OQ-005 tại cổng BRD (xác nhận hoặc sửa P1–P4); agent cập nhật BRD theo quyết định và bỏ các nhãn `[Unverified]`. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking (quyết định của PO tại cổng; là điều kiện duyệt ở §4.14, không phải lỗi của artifact) |
| 19 | 6. Assumptions, Dependencies & Risks | Dependencies & Constraints | Pass | DEP-001..005 dòng 247–251: dịch vụ ngôn ngữ, văn bản mẫu, golden set + người chấm, mạng nội bộ, PO có mặt | Không cần hành động | PO (Phùng Duy Hùng) | Non-blocking |
| 20 | 6. Assumptions, Dependencies & Risks | Business Risks & Mitigation | Pass | RSK-001..004 dòng 255–258 có mức độ, giảm thiểu, dự phòng, owner. Lưu ý: dự phòng RSK-003 "Gỡ văn bản xấu khỏi kho thủ công" trong khi "gỡ văn bản khỏi kho" đang là Deferred (dòng 131); bảng rủi ro không còn cột hạn | Ghi rõ "thủ công" là thao tác ngoài sản phẩm (hoặc đưa việc gỡ văn bản vào phạm vi); thêm hạn cho mỗi RSK. Hạn 2026-11-02 | PO (Phùng Duy Hùng) | Non-blocking |

## Tóm tắt

| Pass | Partial | Fail | N/A | Tổng |
|---|---|---|---|---|
| 18 | 2 | 0 | 0 | 20 |

**Blocking:** không có. Mục 18 (OQ-005) là quyết định của PO tại cổng, owner PO, hạn 2026-11-02. Mục 2 nên được gộp vào cùng quyết định đó.

## Kiểm theo §6 self-check và §7.3 / §7.4 của prompt

### §6 self-check

| Mục | Kết quả | Bằng chứng |
|---|---|---|
| Mỗi BO có ít nhất một BR và metric đo được | Đạt | BO-001..004 → BR-009, BR-005..007/013/015, BR-004/008, BR-016 (dòng 266–269) |
| Mỗi BR dùng `shall`, một nghĩa vụ, không ngôn ngữ giải pháp | Đạt | Dòng 168–193 |
| Mỗi BR có AC và phương pháp kiểm | Đạt | AC-001..016 dòng 199–214; cột Verification |
| Mỗi BR truy về BO hoặc SN, không orphan | Đạt | Đếm lại theo cột Source; xem lệch nhỏ ở mục 13 |
| Scope, exclusions, assumptions, dependencies, risks đều có | Đạt | §4.5, §4.10 |
| Mỗi OQ có owner và hạn | Đạt | OQ-001..005 dòng 284–288 |
| Sponsor xác nhận problem và outcome | Chờ | §4.14 dòng 315 "(chờ)" — việc của PO tại cổng |
| Điểm checklist được báo cáo kèm artifact | Đạt (bằng tham chiếu) | §4.15 dòng 321 trỏ tới `brd-audit.md` |

### §7.3 (ngoài bảng chấm)

- Glossary, coverage, OQ có "Vì sao quan trọng" và Resolution, tham chiếu có phiên bản, điều kiện duyệt + phiên bản baseline: đã sửa (dòng 282–288, 294–307, 311).
- Must requirement không còn check nào hỏng.
- Ngoài BRD (không thuộc phạm vi sửa của vòng này): `interviews/SRC-005.md` dòng 23 vẫn ghi Q7 "Dùng cho: BR-001, BRU-005", trong khi BRU-005 nay lấy nguồn từ P4. Owner PO nên sửa cột này để hồ sơ elicitation không gợi ý PO đã nói về tên tệp trùng ở Q7.

### §7.4 anti-patterns

| Anti-pattern | Có xuất hiện? | Bằng chứng |
|---|---|---|
| Assumptions presented as facts | Một phần | BRU-003/004/005 đã gắn `[Unverified]`; còn target MET-007 và cỡ golden set (mục 2) |
| Open questions resolved silently in the text | Không | BRU-005 nay thuộc OQ-005 |
| "Improve … by X %" with no baseline | Không | Baseline vắng đều có lý do (dòng 94–95) |
| Requirements with no source | Không | — |
| Compound requirement | Không | — |
| Unverifiable wording / solution prescription | Không | — |
| Scope only by inclusion | Không | — |

## Verdict

**Gate ready** về phía audit: 0 Fail, 0 Blocking. Còn 2 Partial, cả hai đều thuộc quyết định của PO tại cổng (owner PO, hạn 2026-11-02):

- mục 18 — OQ-005;
- mục 2 — target MET-007 và cỡ golden set, nên đưa vào OQ-005.

Theo §4.14 dòng 311, BRD chỉ được duyệt (lên v1.0, tag `requirements-v1`) sau khi PO quyết OQ-005. Ngoài OQ-005, không còn gì chặn. Auditor không duyệt; quyết định là của PO.


## Quyết định tại cổng (ghi bởi agent theo lời PO, 2026-11-02)

- PO xác nhận OQ-005 (P1–P4, hồ sơ người dùng): Partial ở row 18 đã được giải quyết.
- Row 2: target MET-007 và cỡ golden set được gắn `[Unverified: OQ-006]`, owner là PO, cần trước chặng Test. Không chặn.
- PO duyệt BRD v1.0, baseline `requirements-v1`. Auditor không duyệt.
