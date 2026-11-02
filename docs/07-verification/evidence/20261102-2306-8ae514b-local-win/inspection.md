# Inspection record — run as in folder name

| TC | Item | Evidence | Result |
|---|---|---|---|
| TC-023 | "Hỏi lại" resends the same question | `web/app.js`: on error, `retry.onclick = () => ask(question, turn)`; the question text is kept in the turn | PASS |
| TC-027 | Listens on localhost only by default; HTTPS/IP restriction documented for deployment | UI test started with `uvicorn app.main:app --host 127.0.0.1`; SAD §4.1, §4.5 describe reverse proxy HTTPS + internal IP range; no auth by decision OQ-002 (NFR-008); encryption N/A in capstone (NFR-009, SAD §4.1) | PASS |
| TC-029 | Vietnamese UI | All app strings come from `web/vi.json` and `app/domain/errors.py`; screenshots show Vietnamese. Exception: the browser-native file control shows "Choose Files / No file chosen" (ui-too-many.jpg) → DEF-002 (Minor) | PASS with DEF-002 |
| TC-030 | Layering | `tests/unit/test_import_rules.py` PASS in pytest.txt | PASS |
| — | FR-004 failed documents in the list | Failures after opening the PDF (scan, password, corrupted) are listed with reason (ui-documents.txt). Files rejected before opening (not_pdf, duplicate, too large, collection full) are reported only in the upload result (ui-upload-response.txt) → DEF-003 (Minor) | Observation |
