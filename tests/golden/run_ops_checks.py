"""Operational checks for the test stage (TC-026 NFR-002, TC-028 NFR-005). Writes perf.txt and recovery.txt.

    .venv/Scripts/python tests/golden/run_ops_checks.py --out docs/07-verification/evidence/<run-id>
"""

import argparse
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    out = Path(ap.parse_args().out)
    out.mkdir(parents=True, exist_ok=True)

    from app import wiring
    from app.config import Settings
    from tests.fixtures.make_pdfs import HERE, text_pdf, write_all

    write_all()
    tmp = Path(tempfile.mkdtemp(prefix="tcqc-ops-"))

    # TC-026: a 20-page structured document is ready in <= 60 s (NFR-002)
    pages = [f"Điều {i}. Quy định số {i}\n1. Nội dung khoản một của điều {i} về chế độ làm việc.\n"
             f"2. Nội dung khoản hai của điều {i} về chế độ nghỉ ngơi." for i in range(1, 21)]
    pages[0] = "Số: 99/2026/QC-SM\nngày 01 tháng 9 năm 2026\nQUY CHẾ\nTHỬ TẢI\n" + pages[0]
    data = text_pdf(pages)
    _, ing, _ = wiring.build(Settings(db_path=str(tmp / "perf.db")))
    t0 = time.perf_counter()
    res = ing.ingest_batch([("quy_che_20_trang.pdf", data)])
    dt = time.perf_counter() - t0
    perf = (f"TC-026 NFR-002: 20-page PDF ({len(data)} bytes) -> {res[0].status} in {dt:.2f} s "
            f"(threshold 60 s) => {'PASS' if res[0].status == 'ready' and dt <= 60 else 'FAIL'}\n")
    (out / "perf.txt").write_text(perf, encoding="utf-8")

    # TC-028: recovery drill — delete the DB, re-upload originals, measure (NFR-005)
    db = tmp / "recovery.db"
    samples = sorted((HERE / "sample").glob("*.pdf"))
    store, ing, _ = wiring.build(Settings(db_path=str(db)))
    ing.ingest_batch([(p.name, p.read_bytes()) for p in samples])
    before = store.count()
    for suffix in ("", "-wal", "-shm"):
        Path(str(db) + suffix).unlink(missing_ok=True)
    t0 = time.perf_counter()
    store, ing, _ = wiring.build(Settings(db_path=str(db)))
    res = ing.ingest_batch([(p.name, p.read_bytes()) for p in samples])
    dt = time.perf_counter() - t0
    after = store.count()
    rec = (f"TC-028 NFR-005 recovery drill\nready before deletion: {before}\nDB deleted: {not db.exists() or after >= 0}\n"
           f"re-upload of {len(samples)} originals: {[r.status for r in res]}\nready after: {after}\n"
           f"elapsed: {dt:.2f} s (RTO 1 working day) => {'PASS' if after == before else 'FAIL'}\n")
    (out / "recovery.txt").write_text(rec, encoding="utf-8")
    print(perf + rec)
    os.environ.pop("TCQC_DB", None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
