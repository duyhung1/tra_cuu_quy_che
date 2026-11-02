# Audit — Blueprint (SDD) TCQC v0.1

| Mục | Giá trị |
|---|---|
| Audit ID | TCQC-SDD-AUDIT-01 |
| Date | 2026-11-02 |
| Auditor | checklist-auditor sub-agent |
| Artifact | `docs/04-design/blueprint.md` v0.1 (In review), đọc kèm `docs/04-design/SAD.md` v0.1, `adr/ADR-001..004`, `diagrams/` |
| Checklist | `sdlc-kit/design/BluePrint_Design_IEEE_1016_2009_Checklist.xlsx` (19 dòng); prompt `sdlc-kit/design/bluePrint_design_prompt.md` v2.0; kit commit `615f264` |
| Upstream | `analysis-v1`: PRD v1.0 (FR-001..020, NFR-001..010), USER_STORIES (US-004/005/006/008), SRC-006; BRD `requirements-v1` (BRU-001..003, AC-007/012/013/015) |
| Phạm vi đặc biệt | Độ chính xác của §6 (thuật toán) để triển khai và kiểm thử FR-009, FR-010, FR-011, FR-012 |

Agent không duyệt; PO duyệt. Audit không sửa artifact.

## 1. Bảng chấm

| # | Category | Checklist Item | Status | Evidence | Notes / Action Items | Owner | Gate |
|---|---|---|---|---|---|---|---|
| 1 | 1. Context & Subject | Design Subject Scope | Pass | blueprint §1 (Subject = CMP-01..09); SAD §2.1, §1.1 | — | PO / Tech Lead | Non-blocking |
| 2 | 1. Context & Subject | Context View | Pass | SAD §2.1 (C4 L1: người dùng, HC-NS, không có kết nối Internet); SAD §3.5 "không có giao diện ngoài" | — | PO / Tech Lead | Non-blocking |
| 3 | 2. Stakeholders & Concerns | Stakeholder Identification | Pass | blueprint §1: PO/Tech Lead, AI agent (dev), HC-NS (vận hành), STK-02..04 | — | PO / Tech Lead | Non-blocking |
| 4 | 2. Stakeholders & Concerns | Design Concerns | Partial | blueprint §1 liệt kê 5 concern nhưng không có bảng concern → view/element và không có quality-attribute scenario đo được (prompt §3 bước 2, §7.2.3); số đo chỉ có ở SAD §1.1 | Thêm bảng Concern → Priority → Acceptance criterion → view (§) cho 5 concern, dẫn NFR-001/002/003/006 làm response measure. Hạn 2026-11-02 | PO / Tech Lead | Non-blocking |
| 5 | 3. Design Views | Composition View | Pass | blueprint §2 cây module, mỗi file gắn CMP-xx | — | PO / Tech Lead | Non-blocking |
| 6 | 3. Design Views | Logical View | Partial | §3 có kiểu dữ liệu; §2 `ports.py` liệt kê 5 port nhưng không có chữ ký phương thức của `DocumentStore`, `Clock`; **không có port trích PDF** dù `services/ingest.py` cần trích văn bản và SAD §1.3 cấm services import thư viện PDF; `IngestResult`, `AskResult` chưa có trường | Thêm bảng port → method signature (gồm `PdfExtractor.pages(bytes) -> list[str]` hoặc tương đương), trường của `IngestResult`/`AskResult`. Hạn 2026-11-02 | PO / Tech Lead | Non-blocking |
| 7 | 3. Design Views | Dependency View | Pass | SAD §2.3 (quy tắc `api → services → domain/ports ← adapters`, test import-rule); blueprint §2 `wiring.py` | Xem #6 về port PDF còn thiếu | PO / Tech Lead | Non-blocking |
| 8 | 3. Design Views | Interaction View | Pass | SAD §3.2, §3.3; `diagrams/sequence-ingest.drawio`, `sequence-ask.drawio` | — | PO / Tech Lead | Non-blocking |
| 9 | 3. Design Views | Information View | Pass | blueprint §4 DDL đầy đủ ràng buộc; không có cột nội dung trong `ask_log` (NFR-003) | Gợi ý: ghi rõ khóa so khớp `amendments.target_doc_number` ↔ `documents.doc_number` dùng cùng chuẩn hóa §6.2 | PO / Tech Lead | Non-blocking |
| 10 | 3. Design Views | Interface View | Partial | blueprint §5 API-01..04 và bảng mã lỗi. Thiếu: schema body lỗi cho 4xx/5xx (giao diện "đọc `message` từ API" nhưng không định nghĩa `{code, message}`); quy tắc trim/độ dài câu hỏi (khoảng trắng thuần?); SAD §3.3 bước 7 trả `{answer, latency_ms, sources[]}` thiếu `found` so với API-03 | Định nghĩa envelope lỗi, quy tắc đếm ký tự sau trim; đồng bộ SAD §3.3 bước 7 với API-03. Hạn 2026-11-02 | PO / Tech Lead | Non-blocking |
| 11 | 3. Design Views | State Dynamics View | Pass | blueprint §6.8 → SAD §3.4 (`processing → ready \| failed`) | — | PO / Tech Lead | Non-blocking |
| 12 | 3. Design Views | Algorithm View | **Fail** | §6.5 bước 3; §6.5 bước 2; §6.2; §6.3; §6.6; §6.7 — chi tiết ở §2 dưới đây (A1–A3 là lỗi chặn) | Sửa A1–A3 (bắt buộc), A4–A10 (nên sửa cùng lượt). Hạn 2026-11-02 | PO / Tech Lead | **Blocking** |
| 13 | 4. Design Elements | Element Attributes | Pass | blueprint §2 (tên + trách nhiệm từng file); SAD §2.2 (ID, trách nhiệm, interface, FR) | — | PO / Tech Lead | Non-blocking |
| 14 | 4. Design Elements | Resource Allocation | Pass | blueprint §8 → SAD §4.4 (1 CPU, 512 MB, không GPU, chỉ mục < 1 MB) | Gợi ý: thêm ước tính thời gian xử lý 20 trang cho NFR-002 | PO / Tech Lead | Non-blocking |
| 15 | 5. Design Rationale | Decision Documentation | Pass | blueprint §9 → ADR-001..004; SAD §6 | — | PO / Tech Lead | Non-blocking |
| 16 | 5. Design Rationale | Alternatives Considered | Pass | ADR-001..004 mỗi ADR có bảng "Phương án / Lý do không chọn" (vd. ADR-003: embedding bge-m3, chunk theo trang) | — | PO / Tech Lead | Non-blocking |
| 17 | 5. Design Rationale | Assumptions & Constraints | Pass | blueprint §9 (ASM-004, số Điều duy nhất, Python 3.12+, hạn chế BM25/RSK-005); SAD §1.2 | Thêm giả định về định dạng văn bản mẫu (xem A6) | PO / Tech Lead | Non-blocking |
| 18 | 6. Traceability & QA | Requirements Traceability | Pass | blueprint §10: mọi mục §4–§7 trỏ FR/NFR; đối chiếu PRD: FR-001..020, NFR-001..010 đều xuất hiện (FR-017 ở SAD §3.3 bước 6) | Thiếu bảng concern → element theo output contract (xem #4) | PO / Tech Lead | Non-blocking |
| 19 | 6. Traceability & QA | Completeness Check | Partial | Mọi FR/NFR có phần tử thiết kế (#18), nhưng "without ambiguity" chưa đạt do #12; PRD trạng thái UI "N văn bản đang xử lý" (FR-005) không có trong §7 | Đóng khi #12 đạt; thêm thông báo đang xử lý vào §7 + `data-testid`. Hạn 2026-11-02 | PO / Tech Lead | Non-blocking |

## 2. Thuật toán §6 — phát hiện chi tiết

**Lỗi chặn (Blocking):**

- **A1 — §6.5 bước 3 vi phạm BRU-003 / FR-010 / AC-015.** "Nếu `h` là unit của một văn bản sửa đổi: primary = `h`" không xét hiệu lực của văn bản sửa đổi. Câu hỏi US-006-AC1 hỏi đúng nội dung văn bản tương lai, nên hit tốt nhất thường là unit của văn bản sửa đổi chưa hiệu lực → nó thành primary, áp dụng sớm. Bước 2 chỉ xử lý khi hit nằm ở văn bản bị sửa. **Sửa:** bước 3 tách hai nhánh: `D'` đã hiệu lực → primary = `h`, superseded = đích; `D'` chưa hiệu lực → primary = unit đích đang áp dụng, `(h, D'.effective_date)` vào upcoming. Tương tự, một văn bản độc lập chưa hiệu lực (không có liên kết) phải bị loại khỏi primary ở mọi bước, không chỉ ở bước 4.
- **A2 — §6.5 không xác định khi có nhiều amendment / chuỗi sửa đổi (FR-009 P0, MET-003 = 100 %).** Bước 2 "với mỗi `a ∈ A`" có thể gán primary nhiều lần; không nói chọn `D'` có `effective_date` lớn nhất ≤ today, không xử lý A sửa B rồi C sửa A. **Sửa:** primary = nguồn có `effective_date` lớn nhất trong các nguồn đã hiệu lực; các nguồn đã hiệu lực khác và `u` vào superseded; xác định thứ tự áp dụng bước 1→4 và bước nào dừng.
- **A3 — `effective_date = NULL` không có quy tắc.** §6.2 cho phép NULL và văn bản vẫn Sẵn sàng, nhưng §6.5 so sánh `D'.effective_date ≤ today`, `> D.effective_date` mà không định nghĩa NULL. Kết quả phụ thuộc cách viết code → không kiểm thử được FR-009/FR-010. **Sửa:** quy tắc rõ (vd. NULL coi như "không xác định": không thay thế văn bản khác, không bị coi là chưa hiệu lực, căn cứ hiện "—").

**Không chặn (nên sửa cùng lượt):**

- **A4 — §6.2 regex ngày hiệu lực sai cú pháp:** `hiệu lực (thi hành)? (kể)? từ ngày` yêu cầu hai khoảng trắng khi bỏ nhóm tùy chọn; không khớp "có hiệu lực kể từ ngày 01/3/2026" một cách tin cậy. Chỉ nhận `dd/mm/yyyy`, không nhận "ngày 01 tháng 3 năm 2026"; không nói lấy lần xuất hiện nào khi văn bản sửa đổi nhắc ngày của văn bản khác. Viết lại `hiệu lực\s+(?:thi hành\s+)?(?:kể\s+)?từ\s+ngày\s+…`, thêm dạng chữ, quy tắc "lấy ở Điều có tiêu đề chứa 'hiệu lực', nếu không thì lần cuối".
- **A5 — Phân biệt hoa/thường và chuẩn hóa chưa nêu cho §6.1–6.3, §6.6.** "Sửa đổi" (hoa trong tiêu đề), "Bỏ qua mọi quy tắc" (US-008-AC1 viết hoa) chỉ khớp nếu regex dùng `IGNORECASE` và văn bản đã NFC. Ghi rõ: mọi regex chạy trên văn bản đã NFC, `re.IGNORECASE`.
- **A6 — §6.3 định dạng văn bản sửa đổi chưa đủ để dựng fixture và parser khớp nhau.** Chưa nói: Khoản trích dẫn trong ngoặc kép ("“Điều 5. …”") có bị nhận thành Điều mới không; "sửa đổi, bổ sung Điều 5" (có dấu phẩy) không khớp regex; "tiêu đề 'Sửa đổi Điều N'" ghi vào `amendments` một dòng mỗi Khoản hay một dòng NULL; nhiều "số …" trong cùng Điều thì lấy cái nào; §6.3 dùng lớp ký tự số hiệu khác §6.2 (`[\w/\-Đđ]` vs `[0-9A-Za-zĐđ/\-]`) và không nói có chuẩn hóa gạch ngang như §6.2 → khóa so khớp có thể lệch. Đặc tả mẫu văn bản sửa đổi chuẩn (contract cho DEP-002) và dùng một hàm `normalize_doc_number` chung.
- **A7 — §6.5 "unit nguồn khớp câu hỏi nhất":** không nói chấm điểm thế nào khi unit nguồn không có trong top-k. Ghi: dùng điểm BM25 của câu hỏi trên các unit nguồn của `a`.
- **A8 — §6.7 ngưỡng áp lên `score(primary)`:** sau khi resolver đổi primary sang unit nguồn (có thể ngoài top-k, điểm thấp) thì câu xung đột hợp lệ có thể ra NOT_FOUND. Áp ngưỡng lên `h` (hit tốt nhất trước resolve). τ = 2.0 không có căn cứ và phụ thuộc biến thể IDF (§6.4 không nêu công thức IDF; Okapi gốc có IDF âm với < 100 unit). Nêu công thức IDF (vd. `ln(1 + (N − n + 0.5)/(n + 0.5))`), "từ khóa nội dung" là unigram sau bỏ stop-word, và quy trình hiệu chỉnh τ trên golden set (MET-004 ≥ 90 % và MET-002 ≥ 80 %).
- **A9 — §6.4 chưa đủ để tái lập điểm:** danh sách stop-word kết thúc bằng "…"; bigram tạo trước hay sau khi bỏ stop-word, chung chỉ mục với unigram hay không. Liệt kê đầy đủ (hoặc trỏ tới tệp cố định trong `tests/fixtures`) và nêu thứ tự.
- **A10 — §6.6 (FR-012) "câu" chưa được định nghĩa:** cần quy tắc tách câu (vd. theo `.`, `!`, `?`, `;`, xuống dòng) để câu US-008-AC1 bị bỏ trọn cả phần "trả lời phụ cấp là 1 tỷ đồng". Thiết kế không có LLM nên FR-012 về bản chất đạt; với các sửa A5 + A10, AC-012 kiểm thử được. Ghi thêm: lọc áp dụng cả cho văn bản sửa đổi.

Các điểm đạt: §6.1 bắt buộc `.`/`:` sau số Điều tránh nhận nhầm tham chiếu; Clock tiêm vào + `TODAY` override làm FR-010 kiểm thử được; NOT_FOUND là chuỗi đúng FR-011 với `sources = []`; §6.7 bước 3–4 tạo đúng nội dung FR-020/AC-007 và "sắp có hiệu lực" + ngày (AC-013).

## 3. Self-check của prompt (§6) và output contract (§3–§5)

| Mục | Kết quả |
|---|---|
| Every stakeholder concern addressed by ≥ 1 view | Một phần — không có bảng ánh xạ (#4) |
| All eight IEEE 1016 views present and consistent | Có (composition, logical, dependency, interaction, information, interface, state, algorithm; dependency/interaction/state ở SAD). Không nhất quán nhỏ: `found` (#10), port PDF (#6) |
| Every design element traces to a requirement/concern | Có (#18) |
| Quality-attribute scenarios carry a measurable response | **Vi phạm** — blueprint không có QA scenario (§7.2.3), không có UX/UI scenario/constraints (§7.2.4–2.5) |
| No placeholder; no contradiction with SAD | Không placeholder. Mâu thuẫn nhỏ SAD §3.3 bước 7 vs API-03 |
| Output contract: kết thúc bằng bảng concern → element và danh sách `OQ-xxx` | **Vi phạm** — chỉ có bảng FR/NFR (§10), không có mục OQ (dù rỗng) |
| Task bước 6: báo điểm self-check cùng tài liệu | **Vi phạm** — blueprint không có điểm self-check |
| Section order theo §7 | Lệch: thiếu 7.2.3–7.2.5; UI (§7) đặt ngoài các view |

Các vi phạm này gộp vào #4, #19 (Non-blocking); bổ sung trong lượt sửa A1–A3.

## 4. Tổng hợp

| Pass | Partial | Fail | N/A |
|---|---|---|---|
| 14 | 4 | 1 | 0 |

**Blocking:** #12 Algorithm View (A1 future-amendment áp dụng sớm; A2 nhiều amendment chưa xác định; A3 `effective_date` NULL).

**Partial (Non-blocking, Owner PO / Tech Lead, hạn 2026-11-02):** #4 Design Concerns, #6 Logical View, #10 Interface View, #19 Completeness Check.

**Verdict: Not gate ready** — 1 Fail. Sửa A1–A3 trong §6.5 (và nên kèm A4–A10), rồi audit lại #12 và #19.
