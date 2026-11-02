# Blueprint (SDD) — Tra cứu quy chế

| Mục | Giá trị |
|---|---|
| Document ID | TCQC-SDD |
| Version | 0.1 |
| Status | In review |
| Owner / Approver | Phùng Duy Hùng (PO, kiêm Tech Lead) |
| Date | 2026-11-02 |
| Prompt | `sdlc-kit/design/bluePrint_design_prompt.md` v2.0 |
| Đầu vào | SAD v0.1, PRD v1.0 (`analysis-v1`) |

## 1. Subject, context, stakeholders

- **Subject:** tiến trình TCQC (CMP-01..09 của SAD §2.2). Ranh giới và context: SAD §2.1.
- **Stakeholders của thiết kế:**
  - PO / Tech Lead (duyệt);
  - AI agent (dev, triển khai theo task);
  - HC-NS (vận hành: đưa lại văn bản khi phục hồi);
  - người dùng (STK-02..04).
- **Concerns:** đúng căn cứ, đúng hiệu lực, không lộ nội dung, độ trễ, hoàn thành trong ngày.

## 2. Composition (module layout)

```
app/
  main.py            CMP-02: FastAPI app, routes, static files
  wiring.py          tạo adapter (chỉ file này import adapters)
  config.py          Settings: DB path, top_k, threshold, timeout, TODAY override
  domain/
    types.py         Document, Unit, Amendment, Hit, Resolution, Source, Answer, UsageRecord, IngestResult
    errors.py        AppError(code) + ERRORS: code → (HTTP status, thông điệp tiếng Việt)
    text.py          normalize, tokenize (giữ dấu tiếng Việt, NFC, lowercase)
  ports.py           DocumentStore, Retriever, Answerer, UsageLog, Clock
  services/
    ingest.py        CMP-03: validate, extract, parse structure, metadata, amendments, instruction filter
    legal_parser.py  CMP-03: Chương/Điều/Khoản, số hiệu, tên, ngày hiệu lực, "Sửa đổi …" (§6.1–6.3)
    resolver.py      CMP-06 (§6.5)
    ask.py           CMP-08: điều phối, timeout, đo thời gian, ghi số liệu
  adapters/
    sqlite_store.py  CMP-04 + CMP-09
    bm25.py          CMP-05 (§6.4)
    rule_answerer.py CMP-07 (§6.7), ADR-001
    pdf_pymupdf.py   trích văn bản theo trang
web/                 CMP-01: index.html, app.js, app.css, vi.json
tests/               unit/, integration/, fixtures/ (văn bản mẫu), golden/
```

## 3. Logical view (kiểu dữ liệu chính)

| Kiểu | Trường | Ghi chú |
|---|---|---|
| `Unit` | id, document_id, chapter, article_no, article_title, clause_no (0 = cả Điều), page, text | Đơn vị truy xuất và căn cứ |
| `Hit` | unit, score, matched_terms | Kết quả CMP-05 |
| `Resolution` | primary: Unit, superseded: list[Unit], upcoming: list[(Unit, date)], score | Kết quả CMP-06 |
| `Source` | ref, filename, doc_title, doc_number, effective_date, article (`"Điều 5"`), clause (`"khoản 1"` hoặc null), page | Phần tử của `sources[]` |
| `Answer` | text, sources: list[Source], found: bool | Kết quả CMP-07 |
| `UsageRecord` | at, latency_ms, status (ok/error), cited_count | Không có trường văn bản |

## 4. Information view (SQLite, ADR-002)

```sql
CREATE TABLE documents (
  id INTEGER PRIMARY KEY,
  filename TEXT NOT NULL UNIQUE,
  title TEXT, doc_number TEXT, effective_date TEXT, signed_date TEXT,   -- ISO yyyy-mm-dd
  pages INTEGER, size_bytes INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('processing','ready','failed')),
  error_code TEXT, units_filtered INTEGER NOT NULL DEFAULT 0,
  uploaded_at TEXT NOT NULL,
  CHECK (status <> 'failed' OR error_code IS NOT NULL)
);
CREATE TABLE units (
  id INTEGER PRIMARY KEY,
  document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chapter TEXT, article_no TEXT, article_title TEXT, clause_no INTEGER NOT NULL DEFAULT 0,
  page INTEGER NOT NULL, text TEXT NOT NULL
);
CREATE TABLE amendments (
  id INTEGER PRIMARY KEY,
  source_unit_id INTEGER NOT NULL REFERENCES units(id) ON DELETE CASCADE,
  target_doc_number TEXT NOT NULL, target_article_no TEXT NOT NULL,
  target_clause_no INTEGER             -- NULL = cả Điều
);
CREATE TABLE ask_log (
  id INTEGER PRIMARY KEY, at TEXT NOT NULL, latency_ms INTEGER NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('ok','error')), cited_count INTEGER NOT NULL
);
```

Không có bảng hay cột nào lưu câu hỏi hoặc câu trả lời (NFR-003).

## 5. Interface view (HTTP API, JSON, tiền tố `/api`)

| ID | Method / path | Request | Response 2xx | Lỗi |
|---|---|---|---|---|
| API-01 | `POST /api/documents` | multipart `files[]` (1–10) | 200 `{items:[{filename, status:"ready", document_id} \| {filename, error_code, message}]}` | 400 `too_many_files` |
| API-02 | `GET /api/documents` | — | 200 `{items:[{id, filename, title, doc_number, effective_date, pages, status, error_code, message}], counts:{ready, failed, total}, limit:50}` | — |
| API-03 | `POST /api/ask` | `{question}` | 200 `{answer, found, latency_ms, sources:[Source]}` | 422 `question_invalid`, 409 `no_documents`, 503 `ai_unavailable` |
| API-04 | `GET /healthz` | — | 200 `{status:"ok"}` | — |

Mã lỗi và thông điệp (một nguồn duy nhất: `app/domain/errors.py`, giao diện đọc `message` từ API):

| code | HTTP | Thông điệp |
|---|---|---|
| `too_many_files` | 400 | Mỗi lần chỉ tải tối đa 10 tệp |
| `not_pdf` | per-file | Không phải tệp PDF hợp lệ |
| `file_too_large` | per-file | Tệp vượt quá 20 MB |
| `too_many_pages` | per-file | Văn bản dài hơn 300 trang |
| `encrypted_pdf` | per-file | Tệp có mật khẩu |
| `no_text_layer` | per-file | PDF dạng ảnh chưa được hỗ trợ |
| `corrupted` | per-file | Tệp bị hỏng |
| `duplicate_name` | per-file | Đã có văn bản cùng tên |
| `collection_full` | per-file | Kho đã đủ 50 văn bản |
| `storage_error` | per-file | Không lưu được văn bản, vui lòng thử lại |
| `question_invalid` | 422 | Câu hỏi phải có từ 1 đến 2000 ký tự |
| `no_documents` | 409 | Chưa có văn bản nào Sẵn sàng để trả lời |
| `ai_unavailable` | 503 | Hệ thống đang bận, vui lòng thử lại |

## 6. Algorithm view

### 6.1 Cấu trúc (Chương / Điều / Khoản)

- **Dòng Điều:** `^Điều\s+(\d+[a-z]?)\s*[.:]\s*(.*)$`. Bắt buộc có `.` hoặc `:` sau số, để câu tham chiếu "theo Điều 5 của …" không bị nhận là tiêu đề.
- **Dòng Chương:** `^Chương\s+([IVXLC]+|\d+)`. Tên chương ở cùng dòng hoặc ở dòng VIẾT HOA ngay sau.
- **Khoản:** dòng `^(\d+)\.\s` bên trong một Điều. Mỗi Khoản là một `Unit` (`clause_no = n`). Điều không có Khoản là một `Unit` với `clause_no = 0`.
- **Tiền tố:** mỗi unit text bắt đầu bằng tiêu đề Điều, để đứng riêng vẫn có nghĩa.
- **Văn bản không có Điều nào:** mỗi trang là một unit (`article_no = NULL`).

### 6.2 Metadata

- **Số hiệu:** `Số\s*[:.]?\s*(\d+/[0-9A-Za-zĐđ/\-]+)` trên trang 1, sau khi chuẩn hóa các loại gạch ngang (soft hyphen, en dash) thành `-`.
- **Tên văn bản:** dòng VIẾT HOA đầu tiên bắt đầu bằng QUY CHẾ / QUYẾT ĐỊNH / NỘI QUY / QUY ĐỊNH / THÔNG BÁO. Nếu dòng chỉ có tên loại thì ghép thêm dòng sau.
- **Ngày ký:** `ngày (\d{1,2}) tháng (\d{1,2}) năm (\d{4})` ở trang 1.
- **Ngày hiệu lực:**
  - lấy từ `hiệu lực (thi hành)? (kể)? từ ngày dd/mm/yyyy`;
  - ghi "hiệu lực kể từ ngày ký" thì bằng ngày ký (BRU-002);
  - không có thì NULL; văn bản vẫn Sẵn sàng và cột hiện "—".

### 6.3 Liên kết sửa đổi

Trong mỗi unit, tìm:

- `(sửa đổi|thay thế)\s+(khoản\s+(\d+)\s+)?Điều\s+(\d+[a-z]?)` kèm số hiệu văn bản đích `số\s+(\d+/[\w/\-Đđ]+)` trong cùng Điều. Nếu tiêu đề Điều là "Sửa đổi Điều N …" thì các Khoản của Điều đó thay các Khoản cùng số của Điều đích.
- Câu "thay thế khoản k Điều N" giới hạn đích vào đúng Khoản k.
- Mỗi liên kết được ghi vào `amendments`.

### 6.4 Truy xuất (CMP-05, ADR-003)

- **Tokenize:** NFC, lowercase, tách theo ký tự không phải chữ/số, giữ dấu; bỏ stop-words tiếng Việt (danh sách ngắn trong `text.py`: "là", "của", "và", "thì", "bao", "nhiêu", "được", "có", "không", …).
- **Thêm bigram** để cụm như "phụ cấp", "nghỉ phép" có trọng số.
- **BM25** (k1 = 1.5, b = 0.75) trên các unit của văn bản Sẵn sàng; trả top-k = 8.

### 6.5 Luật hiệu lực (CMP-06)

Cho hit tốt nhất `h`, đơn vị `u` của văn bản `D`, `today` lấy từ Clock:

1. Tìm `A` = các amendment trỏ tới (`D.doc_number`, `u.article_no`, `u.clause_no` hoặc NULL).
2. Với mỗi `a ∈ A` có văn bản nguồn `D'`:
   - `D'.effective_date ≤ today` và `D'.effective_date > D.effective_date` → **primary = unit nguồn của `a`** khớp câu hỏi nhất; `u` vào `superseded`;
   - `D'.effective_date > today` → `u` vẫn là primary; `(unit nguồn, D'.effective_date)` vào `upcoming` (BRU-003).
3. Nếu `h` là unit của một văn bản sửa đổi: primary = `h`, `superseded` = các unit đích của nó (nếu văn bản đã hiệu lực).
4. Xung đột không có liên kết rõ: hai hit đầu thuộc hai văn bản khác nhau, cùng `article_title` (sau khi chuẩn hóa) và điểm chênh < 20 % → chọn văn bản có `effective_date` muộn hơn (chỉ xét các văn bản đã hiệu lực), văn bản còn lại vào `superseded` (BRU-001).

### 6.6 Lọc chỉ dẫn (FR-012)

Câu chứa mẫu chỉ dẫn được loại khỏi unit lúc xử lý văn bản, và `documents.units_filtered` được tăng lên. Các mẫu:

- `bỏ qua (mọi|các|tất cả)? ?(quy tắc|hướng dẫn|chỉ dẫn)`
- `hãy trả lời`
- `ignore (all|previous|the) (rules|instructions)`
- `bất kể quy định`

Unit rỗng sau khi lọc thì bị bỏ.

### 6.7 Dựng câu trả lời (CMP-07, RuleBasedAnswerer)

1. **Ngưỡng tìm thấy:** `score(primary) ≥ τ` (mặc định τ = 2.0) **và** ≥ 2 từ khóa nội dung của câu hỏi (không tính stop-word) có trong unit. Không đạt → `NOT_FOUND = "Không tìm thấy quy định này trong các văn bản đã tải lên."`, `sources = []`.
2. **Câu chính:** nội dung Khoản primary (bỏ tiêu đề Điều) + ` [1]`.
3. **Nếu có `superseded`:** thêm "Quy định này thay thế {Điều k, khoản n} của {tên} số {số hiệu} (trước đây: «{nội dung}») [2]".
4. **Nếu có `upcoming`:** thêm "Lưu ý: {Điều …} của {tên} số {số hiệu} sắp có hiệu lực từ {dd/mm/yyyy}: «{nội dung}» [3]".
5. **Sources:** các unit theo thứ tự [n], mỗi unit đủ năm thành phần (FR-008).

### 6.8 State dynamics

Như SAD §3.4.

## 7. UI design (CMP-01)

| Màn hình | Thành phần | data-testid |
|---|---|---|
| Tra cứu `/` | Đầu trang: số văn bản đang dùng (liên kết sang Văn bản); luồng hỏi–đáp; khối Căn cứ (`<ol>` [n] Điều — tên · số hiệu · hiệu lực · trang); ô hỏi + bộ đếm x/2000 + nút Gửi; trạng thái bận + "Hỏi lại"; trạng thái khóa khi chưa có văn bản | `ask-input`, `ask-send`, `answer`, `sources`, `retry`, `locked` |
| Văn bản `/#documents` | Vùng chọn tệp (giới hạn ghi rõ); danh sách lỗi theo tệp; bảng Tên · Số hiệu · Hiệu lực · Trang · Trạng thái; tự làm mới 3 giây khi có `processing` | `file-input`, `upload-errors`, `doc-table` |

Mọi chuỗi ở `web/vi.json` (NFR-007). Câu trả lời được chèn bằng `textContent`.

## 8. Resource allocation

Như SAD §4.4. Một tiến trình, không cần GPU, không có mô hình học máy.

## 9. Rationale, alternatives, assumptions

- Quyết định chính: ADR-001..004.
- **Giả định kỹ thuật:**
  - văn bản mẫu dùng cấu trúc §6.1 (ASM-004);
  - số Điều duy nhất trong một văn bản;
  - Python 3.12+ có sẵn trên máy PO.
- **Hạn chế đã biết:**
  - BM25 không hiểu từ đồng nghĩa ("công tác phí" và "phụ cấp lưu trú" chỉ khớp khi văn bản có cả hai từ). Golden set đo hạn chế này (RSK-005).
  - Câu trả lời trích nguyên văn Khoản, không tóm tắt.

## 10. Traceability & completeness

| Design element | FR / NFR |
|---|---|
| §6.1, §6.2 | FR-003 |
| §6.3, §6.5 | FR-009, FR-010, FR-020 |
| §6.4 | FR-005, FR-007, NFR-001 |
| §6.6 | FR-012 |
| §6.7 | FR-007, FR-008, FR-011, FR-019 |
| §4 | FR-004, FR-014, NFR-003 |
| §5 | IF-01..IF-03, FR-001, FR-002, FR-006, FR-013, FR-015, FR-016 |
| §7 | FR-001, FR-004, FR-006, FR-008, FR-013, FR-015, FR-018, NFR-007 |
| SAD §4 | NFR-002, NFR-004..006, NFR-008..010 |

Tất cả FR-001..020 và NFR-001..010 đều có phần tử thiết kế. FR-017 nằm ở SAD §3.3 bước 6.
