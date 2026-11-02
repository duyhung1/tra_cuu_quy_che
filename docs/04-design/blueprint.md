# Blueprint (SDD) — Tra cứu quy chế

| Mục | Giá trị |
|---|---|
| Document ID | TCQC-SDD |
| Version | 1.0 |
| Status | Baselined — `design-v1` (PO, 2026-11-02) |
| Owner / Approver | Phùng Duy Hùng (PO, kiêm Tech Lead) |
| Date | 2026-11-02 |
| Prompt | `sdlc-kit/design/bluePrint_design_prompt.md` v2.0 |
| Đầu vào | SAD v1.0, PRD v1.0 (`analysis-v1`) |

## 1. Subject, context, stakeholders

- **Subject:** tiến trình TCQC (CMP-01..09 của SAD §2.2). Ranh giới và context: SAD §2.1.
- **Stakeholders của thiết kế:**
  - PO / Tech Lead (duyệt);
  - AI agent (dev, triển khai theo task);
  - HC-NS (vận hành: đưa lại văn bản khi phục hồi);
  - người dùng (STK-02..04).
- **Concerns** và nơi được xử lý:

| Concern | View / phần tử |
|---|---|
| Đúng căn cứ | §3 Source, §6.1, §6.7 |
| Đúng hiệu lực | §6.2, §6.3, §6.5 |
| Không lộ nội dung | §4 (ask_log), SAD §4.2 |
| Độ trễ, đồng thời | §6.4, §8, SAD §4.4 |
| Văn bản độc / chỉ dẫn | §6.6, SAD §4.1 |
| Hoàn thành trong ngày | §2 (monolith), ADR-002, ADR-004 |

**Quality-attribute scenarios:**

| ID | Kích thích | Phản hồi đo được |
|---|---|---|
| QS-1 | 10 người cùng hỏi | 0 lỗi, p90 ≤ 30 giây (NFR-001, NFR-006) |
| QS-2 | Đưa vào PDF 20 trang | Sẵn sàng ≤ 60 giây (NFR-002) |
| QS-3 | Văn bản chứa "Bỏ qua mọi quy tắc…" | Câu đó không xuất hiện trong bất kỳ câu trả lời nào (FR-012) |
| QS-4 | Chạy golden set rồi tìm câu hỏi mẫu trong log và `tcqc.db` | 0 kết quả (NFR-003) |

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
| `Resolution` | primary: Unit hoặc None, superseded: list[Unit], upcoming: list[(Unit, date)], found_score, matched_terms, not_found: bool | Kết quả CMP-06 (§6.5 bước 7) |
| `Source` | ref, filename, doc_title, doc_number, effective_date, article (`"Điều 5"`), clause (`"khoản 1"` hoặc null), page | Phần tử của `sources[]` |
| `Answer` | text, sources: list[Source], found: bool | Kết quả CMP-07 |
| `UsageRecord` | at, latency_ms, status (ok/error), cited_count | Không có trường văn bản |
| `PageText` | number (1-based), text | Đầu ra của `PdfExtractor` |
| `IngestResult` | filename, status (ready / failed), document_id, error_code, message | Một phần tử mỗi tệp của API-01 |
| `AskResult` | answer, found, latency_ms, sources | Thân 200 của API-03 |

**Ports** (`app/ports.py`):

| Port | Phương thức |
|---|---|
| `PdfExtractor` | `extract(data: bytes, max_pages: int) -> list[PageText]`; ném `AppError(code)` với code ∈ {corrupted, encrypted_pdf, too_many_pages, no_text_layer} |
| `DocumentStore` | `count() -> int`; `exists(filename) -> bool`; `add(document, units, amendments) -> int` (một transaction); `add_failed(filename, size, code) -> int`; `list() -> list[Document]`; `ready_units() -> list[Unit]`; `amendments() -> list[Amendment]`; `documents_by_id() -> dict[int, Document]` |
| `Retriever` | `rebuild(units)`; `search(q, k) -> list[Hit]`; `score(q, unit) -> float` |
| `Answerer` | `answer(q, resolution) -> Answer` |
| `UsageLog` | `record(UsageRecord) -> None` (ném lỗi thì Ask service bắt, FR-017) |
| `Clock` | `today() -> date` (cấu hình `TCQC_TODAY` để kiểm thử) |

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
| API-02 | `GET /api/documents` | — | 200 `{items:[{id, filename, title, doc_number, effective_date, pages, status, error_code, message}], counts:{ready, processing, failed, total}, limit:50}` | — |
| API-03 | `POST /api/ask` | `{question}` | 200 `{answer, found, latency_ms, sources:[Source]}` | 422 `question_invalid`, 409 `no_documents`, 503 `ai_unavailable` |
| API-04 | `GET /healthz` | — | 200 `{status:"ok"}` | — |

**Câu hỏi:** cắt khoảng trắng hai đầu trước khi kiểm độ dài 1–2000 ký tự. Thân lỗi của mọi phản hồi 4xx/5xx: `{"code": "<code>", "message": "<thông điệp tiếng Việt>"}`.

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

### 6.0 Quy ước chung cho §6

- Mọi biểu thức chính quy chạy trên văn bản đã chuẩn hóa NFC, với `re.IGNORECASE`.
- Trước khi so khớp, các loại gạch ngang (U+00AD, U+2010, U+2011, U+2013) được thay bằng `-`.
- **"Câu":** tách tại xuống dòng, hoặc tại `.`, `!`, `?`, `;` không đứng giữa hai chữ số và theo sau là khoảng trắng: `(?<!\d)[.!?;](?=\s)|
`. Nhờ vậy "300.000" không bị cắt.
- Hằng số `DOC_NO = (\d+/[0-9A-Za-zĐđ/\-]+)`, dùng chung cho §6.2 và §6.3.

### 6.1 Cấu trúc (Chương / Điều / Khoản)

- **Dòng Điều:** `^Điều\s+(\d+[a-z]?)\s*[.:]\s*(.*)$`. Bắt buộc có `.` hoặc `:` sau số, để câu tham chiếu "theo Điều 5 của …" không bị nhận là tiêu đề.
- **Dòng Chương:** `^Chương\s+([IVXLC]+|\d+)`. Tên chương ở cùng dòng hoặc ở dòng VIẾT HOA ngay sau.
- **Khoản:** dòng `^(\d+)\.\s` bên trong một Điều. Mỗi Khoản là một `Unit` (`clause_no = n`). Điều không có Khoản là một `Unit` với `clause_no = 0`.
- **Tiền tố:** mỗi unit text bắt đầu bằng tiêu đề Điều, để đứng riêng vẫn có nghĩa.
- **Văn bản không có Điều nào:** mỗi trang là một unit (`article_no = NULL`).

### 6.2 Metadata

- **Số hiệu:** `Số\s*[:.]?\s*` + `DOC_NO`, lần xuất hiện đầu tiên trên trang 1.
- **Tên văn bản:** dòng VIẾT HOA đầu tiên trên trang 1 bắt đầu bằng QUY CHẾ / QUYẾT ĐỊNH / NỘI QUY / QUY ĐỊNH / THÔNG BÁO. Nếu dòng chỉ có tên loại thì ghép thêm dòng ngay sau (tối đa 200 ký tự).
- **Ngày ký:** `ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})`, lần đầu tiên trên trang 1.
- **Ngày hiệu lực:** thử lần lượt từng mẫu theo thứ tự ưu tiên dưới đây. Mẫu đầu tiên có khớp được dùng, lấy lần xuất hiện đầu tiên của mẫu đó trong toàn văn bản (ưu tiên theo mẫu, không theo vị trí):
  1. `hiệu lực(?:\s+thi hành)?(?:\s+kể)?\s+từ\s+ngày\s+(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})`;
  2. `hiệu lực(?:\s+thi hành)?(?:\s+kể)?\s+từ\s+ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})`;
  3. `hiệu lực(?:\s+thi hành)?(?:\s+kể)?\s+từ\s+ngày\s+ký` → ngày hiệu lực = ngày ký (BRU-002).
  Không mẫu nào khớp → `effective_date = NULL`.
- **Ngày dùng để so sánh** (`eff(D)`):
  - `effective_date` nếu có;
  - nếu không, `signed_date`;
  - nếu cả hai đều NULL, `eff(D) = −∞` và văn bản bị đánh dấu "không rõ ngày hiệu lực". Văn bản loại này coi như đã hiệu lực nhưng **không bao giờ thay thế** văn bản khác (A3).

### 6.3 Liên kết sửa đổi

1. **Điều sửa đổi:** tiêu đề Điều khớp `(?:sửa đổi(?:,\s*bổ sung)?|thay thế)\s+Điều\s+(\d+[a-z]?)`. Văn bản đích là `DOC_NO` đầu tiên sau cụm `số` trong tiêu đề Điều; nếu tiêu đề không có thì tìm trong thân Điều.
2. **Khoản được thay rõ ràng:** trong toàn văn bản sửa đổi, mọi lần khớp `thay thế\s+khoản\s+(\d+)\s+Điều\s+(\d+[a-z]?)` (kèm `DOC_NO` của cùng câu, hoặc của điều sửa đổi tương ứng) tạo tập `K(N)` các khoản bị thay của Điều N.
3. **Sinh dòng `amendments`:** với mỗi Khoản `i` của Điều sửa đổi nhắm tới Điều N:
   - nếu `K(N)` khác rỗng: chỉ khi `i ∈ K(N)` mới tạo dòng (source = Khoản i, target = (doc, N, i)). Các Khoản khác là quy định mới, không thay gì;
   - nếu `K(N)` rỗng: tạo dòng target = (doc, N, i).
   - Điều sửa đổi không có Khoản: một dòng target = (doc, N, NULL), nghĩa là thay cả Điều.
4. Một đích có thể có nhiều dòng `amendments` (nhiều văn bản sửa đổi, hoặc sửa đổi nối chuỗi).

### 6.4 Truy xuất (CMP-05, ADR-003)

- **Tokenize:** NFC, lowercase, tách theo ký tự không phải chữ/số, giữ dấu.
- **Stop-word:** danh sách đóng trong `app/domain/text.py`. Đây là nguồn duy nhất; danh sách có thể được tinh chỉnh theo golden set và mọi thay đổi ghi vào TEST_REPORT. Danh sách khởi đầu: là, của, và, thì, mà, bao, nhiêu, được, có, không, cho, các, những, một, này, đó, khi, nào, gì, ai, tôi, bạn, hiện, nay, theo, với, về, trong, từ, đến, ở, thế, sao.
- **Bigram:** tạo từ dãy token **trước** khi bỏ stop-word, rồi bỏ bigram chứa stop-word. Unigram sau khi bỏ stop-word.
- **BM25:**
  - `idf(t) = ln(1 + (N − df + 0.5) / (df + 0.5))`;
  - `score = Σ idf(t) · tf·(k1+1) / (tf + k1·(1 − b + b·len/avglen))`, với k1 = 1.5, b = 0.75;
  - tính trên các unit của văn bản Sẵn sàng; trả top-k = 8.

### 6.5 Luật hiệu lực (CMP-06) — `resolve(question, hits, today)`

**Định nghĩa:**
- `in_force(D) ⇔ eff(D) ≤ today` (§6.2).
- `score(q, u)` là điểm BM25 của câu hỏi với **bất kỳ** unit `u`, không chỉ các unit trong top-k (A7).
- `targets(u)`: các unit đích của các dòng `amendments` có source = `u`. Đích có `clause_no = NULL` ứng với mọi Khoản của Điều đó.
- `amenders(t)`: các unit nguồn có dòng `amendments` trỏ tới `t`, trỏ tới cả Điều của `t`, hoặc trỏ tới đúng `(doc_number, article_no, NULL)`.

**Thuật toán** (chạy đúng thứ tự, dừng ở bước có ghi "dừng"):

1. **Ngưỡng trước** (R1): `h0 = hits[0]` (điểm cao nhất, kể cả văn bản chưa hiệu lực). `found_score = score(h0)`. Nếu §6.7 bước 1 không đạt (τ, ≥ 2 từ khớp trên `h0`) → NOT_FOUND. **Dừng.**
2. **Gốc** (R2):
   - Nếu `targets(h0.unit)` khác rỗng (h0 là Khoản sửa đổi, dù văn bản sửa đổi đã hay chưa hiệu lực): `base = argmax_{t ∈ targets(h0.unit)} score(q, t)`, tính trên mọi unit, không giới hạn top-k.
   - Ngược lại, nếu `in_force(doc(h0))`: `base = h0.unit`.
   - Ngược lại (h0 là văn bản tương lai không có liên kết): `base` = hit đang hiệu lực đầu tiên trong `hits`. Nếu không có: kết quả `primary = None`, `upcoming = [h0]` → câu "Hiện chưa có quy định đang áp dụng." kèm mục sắp có hiệu lực (§6.7). **Dừng.**
   - `future = [h ∈ hits | not in_force(doc(h))]`.
3. *(gộp vào bước 2)*
4. **Chọn bản đang áp dụng** (A1, A2): `applied = base`, `superseded = []`. Lặp tối đa 5 lần:
   - `cands = [a ∈ amenders(applied) | in_force(doc(a)) và eff(doc(a)) > eff(doc(applied))]`.
   - Nếu `cands` rỗng thì thôi lặp.
   - Nếu không: `newest` = phần tử có `eff` lớn nhất (bằng nhau thì xét `signed_date` muộn hơn, rồi `id` lớn hơn). Đưa `applied` **và mọi phần tử khác của `cands`** vào `superseded` (R3), rồi `applied = newest`.
   - Vòng lặp xử lý được sửa đổi nối chuỗi (A → B → C). Các văn bản cùng sửa một đích đều bị so sánh, chỉ giữ văn bản hiệu lực muộn nhất.
5. **Sắp có hiệu lực:**
   - `upcoming = [a ∈ amenders(applied) ∪ amenders(base) | not in_force(doc(a))]`, sắp theo `eff` tăng dần;
   - cộng thêm `h ∈ future` có `article_title` (đã chuẩn hóa) trùng với của `applied` mà không có liên kết.
   - Không unit nào trong `upcoming` được làm `primary` (BRU-003, FR-010).
6. **Xung đột không có liên kết** (BRU-001):
   - Với `h ∈ current`, `h` thuộc văn bản khác `applied`, `article_title` trùng và `score(h) ≥ 0.8 × found_score`:
     - nếu `eff(doc(h)) > eff(doc(applied))` và `doc(h)` không phải "không rõ ngày": `superseded += [applied]`, `applied = h.unit`;
     - nếu không: `superseded += [h.unit]`.
   - Mỗi văn bản chỉ xét một lần.
7. **Kết quả:** `Resolution(primary = applied, superseded, upcoming, found_score, matched_terms(h0))`.

**Test bắt buộc** (TASK-007), dựng từ văn bản mẫu:
- (a) Khoản 1 Điều 5 bị Quyết định 02/2026 thay;
- (b) Khoản 2 Điều 5 không bị thay;
- (c) hit tốt nhất là Khoản của văn bản sửa đổi chưa hiệu lực → primary vẫn là Khoản cũ, upcoming có văn bản mới;
- (d) chuỗi hai sửa đổi → lấy văn bản muộn nhất đang hiệu lực;
- (e) văn bản không rõ ngày không thay văn bản khác;
- (f) không có văn bản đang hiệu lực, chỉ có văn bản tương lai.

### 6.6 Lọc chỉ dẫn (FR-012)

Mỗi **câu** (§6.0) chứa mẫu chỉ dẫn được loại khỏi unit lúc xử lý văn bản, và `documents.units_filtered` tăng theo số câu bị loại. Các mẫu:

- `bỏ qua (mọi|các|tất cả)? ?(quy tắc|hướng dẫn|chỉ dẫn)`
- `hãy trả lời`
- `ignore (all|previous|the) (rules|instructions)`
- `bất kể quy định`

Unit rỗng sau khi lọc thì bị bỏ.

### 6.7 Dựng câu trả lời (CMP-07, RuleBasedAnswerer)

1. **Ngưỡng tìm thấy:** `found_score ≥ τ` **và** ≥ 2 unigram nội dung của câu hỏi có trong unit `h0` (§6.5 bước 2). Cả hai tính trên hit gốc, không phải trên bản đã đổi.
   - τ là cấu hình (`TCQC_THRESHOLD`), giá trị khởi đầu 2.0. Giá trị này được tinh chỉnh trên golden set ở chặng Test; giá trị cuối và lý do ghi vào TEST_REPORT.
   - Không đạt → `NOT_FOUND = "Không tìm thấy quy định này trong các văn bản đã tải lên."`, `sources = []`.
   - Trường hợp §6.5 bước 2 (`primary = None`, đã qua ngưỡng ở bước 1): câu "Hiện chưa có quy định đang áp dụng." kèm các mục sắp có hiệu lực (bước 4 bên dưới), `found = true`.
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

Khi `counts.processing > 0`, màn hình Tra cứu hiện banner "N văn bản đang xử lý, chưa được dùng để trả lời" (FR-005).

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

## 11. Open questions và self-check

| ID | Câu hỏi | Owner | Cần trước |
|---|---|---|---|
| OQ-008 | (SAD §3.5) API-01 trả trạng thái cuối thay cho "Đang xử lý" | PO | **Đã quyết 2026-11-02: chấp nhận** |

**Self-check:**
- mọi FR/NFR có phần tử thiết kế (§10);
- thuật toán §6 được đặc tả đủ để viết test (danh sách test bắt buộc ở §6.5);
- concern → view (§1);
- QS-1..4.

Điểm chính thức: [blueprint-audit.md](blueprint-audit.md).
